from django.db import models
from django.utils.translation import gettext_lazy as _

class MedicineUnit(models.TextChoices):
    VIEN = 'Vien', _('Viên')
    GOI = 'Goi', _('Gói')
    CHAI = 'Chai', _('Chai')
    ONG = 'Ong', _('Ống')
    TUYP = 'Tuyp', _('Tuýp')
    VI = 'Vi', _('Vỉ')

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10, choices=MedicineUnit.choices)
    effect = models.TextField()
    current_selling_price = models.DecimalField(max_digits=12, decimal_places=2)

class MedicineBatch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    import_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_imported = models.PositiveIntegerField()
    quantity_remaining = models.PositiveIntegerField()
    expiry_date = models.DateField()
    import_date = models.DateField()

class Prescription(models.Model):
    medical_result = models.OneToOneField('clinical.MedicalResult', on_delete=models.CASCADE)
    doctor_advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PrescriptionDetail(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    dosage = models.CharField(max_length=255)