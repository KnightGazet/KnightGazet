from django.shortcuts import render

# Create your views here.
# Manually added code here

from django.shortcuts import  get_object_or_404
from .models import Doctor, Patient, Appointment, MedicalRecord
from django.http import JsonResponse

def doctor_list(request):
    doctors = Doctor.objects.all()
    return JsonResponse({"doctors": list(doctors.values())})

def patient_list(request):
    patients = Patient.objects.all()
    return JsonResponse({"patients": list(patients.values())})

def appointment_list(request):
    appointments = Appointment.objects.all()
    return JsonResponse({"appointments": list(appointments.values())})

def medical_records(request, patient_id):
    records = MedicalRecord.objects.filter(patient_id=patient_id)
    return JsonResponse({"records": list(records.values())})