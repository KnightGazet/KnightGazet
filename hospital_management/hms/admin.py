from django.contrib import admin

# Register your models here.
# Manually added code

from .models import Doctor, Patient, Appointment, MedicalRecord

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)