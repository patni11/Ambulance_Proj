from django.contrib import admin
from .models import Ambulance, Patient, PatientArchive
from django.apps import apps
# Register your models here.


class AmbulanceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("State", {"fields": ["ambulance_state"]}),
        ("Location", {"fields": [
         "ambulance_lat", "ambulance_long"]}),
        ("Time", {"fields": [
         "ambulance_pickup_time", "ambulance_free_est_time"]}),
    ]


admin.site.register(Ambulance, AmbulanceAdmin)
admin.site.register(Patient)
admin.site.register(PatientArchive)
