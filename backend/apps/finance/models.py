from django.db import models
from django.utils.translation import gettext_lazy as _

class PaymentStatus(models.TextChoices):
    UNPAID = 'UNPAID', _('Chưa thanh toán')
    PAID = 'PAID', _('Đã thanh toán')
    REFUNDED = 'REFUNDED', _('Đã hoàn tiền')

class Invoice(models.Model):
    patient = models.ForeignKey('accounts.Patient', on_delete=models.PROTECT)
    medical_result = models.ForeignKey('clinical.MedicalResult', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)