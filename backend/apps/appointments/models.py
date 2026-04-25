from django.db import models
from django.utils.translation import gettext_lazy as _

class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', _('Đang chờ')
    CONFIRMED = 'CONFIRMED', _('Đã xác nhận')
    COMPLETED = 'COMPLETED', _('Hoàn thành')
    CANCELLED = 'CANCELLED', _('Đã hủy')

class AppointmentType(models.TextChoices):
    ONLINE = 'ONLINE', _('Trực tuyến')
    OFFLINE = 'OFFLINE', _('Tại phòng khám')

class Schedule(models.Model):
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE)
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.PositiveIntegerField()
    current_patients = models.PositiveIntegerField(default=0)

class Appointment(models.Model):
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE)
    specialty = models.ForeignKey('master_data.Specialty', on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meeting_link = models.URLField(blank=True, null=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    type = models.CharField(max_length=10, choices=AppointmentType.choices)
    created_at = models.DateTimeField(auto_now_add=True)