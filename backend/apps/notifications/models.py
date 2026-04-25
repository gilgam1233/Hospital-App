from django.db import models
from django.utils.translation import gettext_lazy as _

class NotificationType(models.TextChoices):
    REMINDER = 'REMINDER', _('Nhắc hẹn')
    RESULT = 'RESULT', _('Kết quả')
    SYSTEM = 'SYSTEM', _('Hệ thống')
    PRESCRIPTION = 'PRESCRIPTION', _('Đơn thuốc')

class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)