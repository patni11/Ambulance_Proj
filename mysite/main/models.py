from django.db import models
from django.utils.timezone import now
# Create your models here.


class Ambulance(models.Model):
    ambulance_state = models.BooleanField()
    ambulance_lat = models.DecimalField(max_digits=10, decimal_places=6)
    ambulance_long = models.DecimalField(max_digits=10, decimal_places=6)
    ambulance_free_est_time = models.DateTimeField(
        "Estimated Time for Next Patient")
    ambulance_pickup_time = models.DateTimeField("Pickup Time")

    def __str__(self):
        if self.ambulance_state:
            state = "OCCUPIED"
            next_available = f"IT WILL BE AVAILABLE IN {str(self.ambulance_pickup_time)}"

        else:
            state = "AVAILABLE"
            next_available = ""

        return f"AMBULANCE IS {state}"

# class DriverSide(models.Model):


class PatientArchive(models.Model):
    name = models.CharField("Patient Name", max_length=50)
    caretaker_name = models.CharField("Caretaker Name", max_length=50)

    contact_num = models.DecimalField(
        "Enter Your Phone Number", max_digits=10, decimal_places=0)

    pickup_location = models.CharField("Enter Pickup Location", max_length=70)
    drop_location = models.CharField("Enter Drop Location", max_length=70)

    time_created = models.DateTimeField()

    def __str__(self):
        return f"{self.name} was treated on {time_created}"


class Patient(models.Model):
    """FORM FIELDS"""
    name = models.CharField("Patient Name", max_length=50)
    caretaker_name = models.CharField("Caretaker Name", max_length=50)

    contact_num = models.DecimalField(
        "Enter Your Phone Number", max_digits=10, decimal_places=0)

    pickup_location = models.CharField("Enter Pickup Location", max_length=70)
    drop_location = models.CharField("Enter Drop Location", max_length=70)

    time_created = models.DateTimeField(default=now)

    next_patient_to_pick_up = models.BooleanField(default=False)
    patient_picked_up = models.BooleanField(default=False)
    patient_delivered = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.name} is Patient"
    # We will later look at other fields
