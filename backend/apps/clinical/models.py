from django.db import models

class MedicalResult(models.Model):
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    clinical_notes = models.TextField()
    re_examination_date = models.DateField(null=True, blank=True)

class LabResult(models.Model):
    medical_result = models.ForeignKey(MedicalResult, on_delete=models.CASCADE)
    lab_service = models.ForeignKey('master_data.LabService', on_delete=models.CASCADE)
    result_value = models.TextField()
    result_img = models.ImageField(upload_to='lab_results/', null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)