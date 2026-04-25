from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# ==========================================
# 0. DANH MỤC ENUM (CONSTANTS)
# ==========================================

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Quản trị viên')
    DOCTOR = 'DOCTOR', _('Bác sĩ')
    PATIENT = 'PATIENT', _('Bệnh nhân')
    STAFF = 'STAFF', _('Nhân viên y tế')
    PHARMACIST = 'PHARMACIST', _('Dược sĩ')

class AppointmentStatus(models.TextChoices):
    PENDING = 'PENDING', _('Đang chờ')
    CONFIRMED = 'CONFIRMED', _('Đã xác nhận')
    COMPLETED = 'COMPLETED', _('Hoàn thành')
    CANCELLED = 'CANCELLED', _('Đã hủy')

class AppointmentType(models.TextChoices):
    ONLINE = 'ONLINE', _('Trực tuyến')
    OFFLINE = 'OFFLINE', _('Tại phòng khám')

class PaymentStatus(models.TextChoices):
    UNPAID = 'UNPAID', _('Chưa thanh toán')
    PAID = 'PAID', _('Đã thanh toán')
    REFUNDED = 'REFUNDED', _('Đã hoàn tiền')

class MedicineUnit(models.TextChoices):
    VIEN = 'Vien', _('Viên')
    GOI = 'Goi', _('Gói')
    CHAI = 'Chai', _('Chai')
    ONG = 'Ong', _('Ống')
    TUYP = 'Tuyp', _('Tuýp')
    VI = 'Vi', _('Vỉ')

class NotificationType(models.TextChoices):
    REMINDER = 'REMINDER', _('Nhắc hẹn')
    RESULT = 'RESULT', _('Kết quả')
    SYSTEM = 'SYSTEM', _('Hệ thống')
    PRESCRIPTION = 'PRESCRIPTION', _('Đơn thuốc')

# ==========================================
# 1. NHÓM DANH MỤC & ĐỊA CHÍNH
# ==========================================

class Country(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=10)
    def __str__(self): return self.name

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

class Ward(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

class Career(models.Model):
    name = models.CharField(max_length=100)

class EthnicGroup(models.Model):
    name = models.CharField(max_length=50)

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    img = models.ImageField(upload_to='specialties/', null=True, blank=True)

class Disease(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

class LabService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

# ==========================================
# 2. NGƯỜI DÙNG & HỒ SƠ
# ==========================================

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PATIENT
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    dob = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)
    street_address = models.CharField(max_length=255)
    citizen_id = models.CharField(max_length=20)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True)
    ethnic_group = models.ForeignKey(EthnicGroup, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='profiles/', null=True, blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
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

# ==========================================
# 3. KHÁM BỆNH & LỊCH HẸN
# ==========================================

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.PositiveIntegerField()
    current_patients = models.PositiveIntegerField(default=0)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meeting_link = models.URLField(blank=True, null=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    type = models.CharField(max_length=10, choices=AppointmentType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class MedicalResult(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    clinical_notes = models.TextField()
    re_examination_date = models.DateField(null=True, blank=True)

class LabResult(models.Model):
    medical_result = models.ForeignKey(MedicalResult, on_delete=models.CASCADE)
    lab_service = models.ForeignKey(LabService, on_delete=models.CASCADE)
    result_value = models.TextField()
    result_img = models.ImageField(upload_to='lab_results/', null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# ==========================================
# 4. DƯỢC PHẨM & THANH TOÁN
# ==========================================

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
    medical_result = models.OneToOneField(MedicalResult, on_delete=models.CASCADE)
    doctor_advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PrescriptionDetail(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    dosage = models.CharField(max_length=255)

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    medical_result = models.ForeignKey(MedicalResult, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID
    )
    created_at = models.DateTimeField(auto_now_add=True)

# ==========================================
# 5. THÔNG BÁO
# ==========================================

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)