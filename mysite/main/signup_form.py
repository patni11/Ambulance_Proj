from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Patient
from django_otp.forms import OTPAuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Phone Number", max_length=10, min_length=10, required=True,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Enter Your Phone Number Here', 'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': 'Enter numbers Only '}))

    class Meta:
        fields = ["username", "password"]


class PatientForm(ModelForm):
    contact_num = forms.CharField(max_length=10, min_length=10, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': 'Enter numbers Only '}))

    class Meta:
        model = Patient
        fields = ['name',  'caretaker_name', 'contact_num', 'pickup_location',
                  'drop_location']


class OTPForm(ModelForm):
    otp = forms.CharField(label="Enter Otp", max_length=6)

    class Meta:
        model = Patient
        fields = ["otp"]


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    USERNAME_FIELD = 'email'
    username = forms.CharField(label="Phone Number", max_length=10, min_length=10, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'pattern': '[0-9]+', 'title': 'Enter numbers Only '}))

    name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("username", "name", "email")

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Phone Number exists, Maybe You Forgot The Pass")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email exists, Maybe you forgot the password")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
