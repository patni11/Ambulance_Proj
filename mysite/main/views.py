from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ambulance, Patient, PatientArchive
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .signup_form import UserForm, PatientForm, OTPForm, LoginForm
from django.contrib.auth.models import User, Group
from .decorators import unautherized_user, allowed_users
from .generate_otp import HandleOTP
from django.utils.timezone import now
import inspect
from twilio.rest import Client
import os
# Create your views here.


def homepage(request):
    availability = True
    patient_num = Patient.objects.all()
    
    if patient_num:
        ambulance = Ambulance.objects.all()[0]
        ambulance.ambulance_state = True
        ambulance.save()

    if len(patient_num) <= 4:
        if request.method == "POST":
            form = PatientForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('name')
                try:
                    otp = HandleOTP().generate_otp()
                    form.otp = otp
                    send_otp_message(otp, form.cleaned_data.get('contact_num'))
                    form.save()
                    send_message(f"Patient booked an ambulance, Here's their number - {form.cleaned_data.get('contact_num')} . use this link - http://192.168.1.38:8000/driver/", 7742361132)
                    messages.success(request, f"Ambulance Successfully Booked For {username}")
                except:
                    messages.error(request,"Probably you entered a wrong number, please try again")
                    return redirect("main:homepage")
    else:
        availability = False
    form = PatientForm()
    
    return render(request=request,
                  template_name="main/user2.html",
                  context={"ambulance_data": Ambulance.objects.all, "form": form, "availability": availability, "patient_len":len(Patient.objects.all())})


def otp_verification(request, user, template):
    form = OTPForm(request.POST or None)
    otp = user.otp
    if not request.POST:
        pass
    else:
        if form.is_valid():
            num = form.cleaned_data.get('otp')
            if str(otp) == num:
                return [True, form]
            else:
                return [False, form]
        else:
            messages.error(
                request, "There was something wrong, please try again")
            return [render(request, template_name=template, context={"form": form})]

    return [render(request, template, context={"form": form})]


def archive_patient(patient):
    archive = PatientArchive()

    archive.name = patient.name
    archive.caretaker_name = patient.caretaker_name
    archive.contact_num = patient.contact_num
    archive.pickup_location = patient.pickup_location
    archive.drop_location = patient.drop_location
    archive.time_created = patient.time_created

    archive.save()

@allowed_users(allowed_roles=["admin"])
def patient_delivered(request):
    if Patient.objects.all()[0]:
        user = Patient.objects.all()[0]
        template = 'main/driver_verification.html'
        return_items = otp_verification(request, user, template)
        try:
            verification, form = return_items[0], return_items[1]
        except:
            return return_items[0]

        if verification:
            user.patient_delivered = True
            messages.success(
                request, "You Saved A Life!")
            user.save()
            archive_patient(user)
            user.delete()
            # send msg to user for new otp
            return redirect("main:driver")
        else:
            messages.error(request, "Wrong Otp")
    else:
        form = "No Patients At The Moment"

    return render(request, 'main/driver_verification.html', context={"form": form})


@allowed_users(allowed_roles=["admin"])
def driver_verification(request,new_otp=None):
    if Patient.objects.all()[0]:
        user = Patient.objects.all()[0]
        template = 'main/driver_verification.html'
        if new_otp != None:
            try:
                otp = HandleOTP().generate_otp()
                user.otp = otp
                user.save()
                send_otp_message(otp, user.contact_num)
                messages.info(request,"Otp Sent Successfully")
            except:
                messages.error(request,"There was some error, please try again")
                return redirect("home:driver_verification")

        return_items = otp_verification(request, user, template)
        try:
            verification, form = return_items[0], return_items[1]
        except:
            return return_items[0]

        if verification:
            user.patient_picked_up = True
            otp2 = HandleOTP().generate_otp()
            user.otp = otp2
            messages.success(
                request, "Thank You")
            user.save()
            send_otp_message(otp2, user.contact_num)
            return redirect("main:driver")
        else:
            messages.error(request, "Wrong Otp")
    else:
        form = "No Patients At The Moment"

    return render(request, 'main/driver_verification.html', context={"form": form})

def resend_otp(request):
    return driver_verification(request,True)

'''
@allowed_users(allowed_roles=["admin"])
def driver_verification(request):
    form = OTPForm(request.POST or None)
    user = Patient.objects.all()[0]
    # pk = request.session.get('pk')
    # print("PK", pk)
    otp = user.otp
    print("OTP", otp)
    if not request.POST:
        pass
    else:
        if form.is_valid():
            num = form.cleaned_data.get('otp')
            if str(otp) == num:
                user.patient_picked_up = True
                otp2 = HandleOTP().generate_otp()
                user.otp = otp2
                messages.success(
                    request, "Thank You")
                user.save()
                # send msg to user for new otp
                return redirect("main:driver")
            else:
                messages.error(request, "Wrong Otp")
        else:
            messages.error(
                request, "There was something wrong, please try again")
            return render(request, 'main/driver_verification.html', context={"form": form})

    return render(request, 'main/driver_verification.html', context={"form": form})
'''


def logout_request(request):
    logout(request)
    messages.info(request, "logged out successully")
    return redirect("main:homepage")


def send_otp_message(otp, phone_number):
    send_message(body = f'Your Otp is {otp}',phone_num = phone_number)

def send_message(body,phone_num):
    account_sid = 'ACb2823447755238ebb4ad39b7ec827ba3'
    auth_token = 'af5009496f1617af1891713c56644caf'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=body,
        from_="+16262494914",
        to=f'+91{phone_num}'
    )


@ allowed_users(allowed_roles=["admin"])
def driver(request):
    if request.GET.get('DeleteButton'):
        
        Patient.objects.filter(id=request.GET.get('DeleteButton')).delete()
        return redirect('main:driver')
    current_patient = []
    patients = Patient.objects.all()
    active_patient = "No Patient Exist"
    if patients:
        for patient in Patient.objects.all():
            if patient.next_patient_to_pick_up == True:
                current_patient.append(patient)
                active_patient = current_patient[0]

        if not current_patient:
            try:
                current_patient_now = Patient.objects.all()[0]
                current_patient_now.next_patient_to_pick_up = True
                current_patient_now.save()
                current_patient.append(current_patient_now)
                active_patient = current_patient[0]

            except Exception:
                print("OTP Error")

    else:
        patients = "No Patients At The Moment"       
        ambulance = Ambulance.objects.all()[0]
        ambulance.ambulance_state = False
        ambulance.save()

    return render(request=request, template_name="main/driver.html", context={"patients": patients, "current_patient": active_patient})


@ unautherized_user
def login_request(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(password=password, username=username)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Successfully Logged In")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid Username Or Pass")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = LoginForm()
    return render(request, "main/login.html", {"form": form})


"""
@ unautherized_user
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(password=password, username=username)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Logged In Successully as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid Username Or Pass")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})
"""


@ unautherized_user
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('name')
            messages.success(request, f"Welcome {username}")
            group = Group.objects.get(name="patient")
            user.groups.add(group)
            login(request, user)
            return redirect("main:homepage")
        else:
            messages.error(request, "Please Fix The Errors First")
    else:
        form = UserForm()
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})
