from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Quản trị viên')
    DOCTOR = 'DOCTOR', _('Bác sĩ')
    PATIENT = 'PATIENT', _('Bệnh nhân')
    STAFF = 'STAFF', _('Nhân viên y tế')
    PHARMACIST = 'PHARMACIST', _('Dược sĩ')

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.PATIENT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField()
    country = models.ForeignKey('master_data.Country', on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey('master_data.Province', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('master_data.District', on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey('master_data.Ward', on_delete=models.SET_NULL, null=True)
    street_address = models.CharField(max_length=255)
    citizen_id = models.CharField(max_length=20)
    career = models.ForeignKey('master_data.Career', on_delete=models.SET_NULL, null=True)
    ethnic_group = models.ForeignKey('master_data.EthnicGroup', on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='profiles/', null=True, blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.ForeignKey('master_data.Specialty', on_delete=models.PROTECT)
    summary = models.TextField()
    experience = models.PositiveIntegerField()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    blood_type = models.CharField(max_length=5)
    height = models.FloatField()
    weight = models.FloatField()
    medical_history = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=30, blank=True)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=15)