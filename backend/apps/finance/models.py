from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class PaymentStatus(models.TextChoices):
    UNPAID = 'UNPAID', _('Chưa thanh toán')
    PAID = 'PAID', _('Đã thanh toán')
    REFUNDED = 'REFUNDED', _('Đã hoàn tiền')


class PaymentMethod(models.TextChoices):
    CASH = 'CASH', _('Tiền mặt')
    TRANSFER = 'TRANSFER', _('Chuyển khoản')

class Invoice(models.Model):
    patient = models.ForeignKey('accounts.Patient', on_delete=models.PROTECT, related_name='invoices')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='processed_invoices')

    medical_result = models.ForeignKey('clinical.MedicalResult', on_delete=models.SET_NULL, null=True, blank=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hóa đơn #{self.id} - {self.patient}"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')

    service = models.ForeignKey('master_data.LabService', on_delete=models.SET_NULL, null=True, blank=True)
    medicine = models.ForeignKey('pharmacy.Medicine', on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def sub_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"Chi tiết của Hóa đơn #{self.invoice_id}"