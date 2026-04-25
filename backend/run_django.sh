#!/bin/bash

echo "=== 1. Cài đặt thư viện từ requirements.txt ==="
pip install -r requirements.txt

echo "=== 2. Thực thi migrate cơ sở dữ liệu ==="
# Ưu tiên các app nền tảng để tránh lỗi khóa ngoại MySQL
python manage.py makemigrations master_data accounts
python manage.py makemigrations
python manage.py migrate accounts
python manage.py migrate

echo "=== 3. Tạo Superuser (Admin) tự động ==="
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@hospital.com
export DJANGO_SUPERUSER_PASSWORD=Admin@123

python manage.py createsuperuser --no-input || echo "SuperUser đã tồn tại!"

echo "=== 4. Chèn dữ liệu cứng (Hardcoded Seed Data) ==="
python manage.py shell <<EOF
from django.apps import apps
from django.contrib.auth import get_user_model
import random

User = get_user_model()

# Lấy các Model từ các app khác nhau
Country = apps.get_model('master_data', 'Country')
Province = apps.get_model('master_data', 'Province')
Specialty = apps.get_model('master_data', 'Specialty')
LabService = apps.get_model('master_data', 'LabService')
Medicine = apps.get_model('pharmacy', 'Medicine')
Profile = apps.get_model('accounts', 'Profile')
Doctor = apps.get_model('accounts', 'Doctor')
Patient = apps.get_model('accounts', 'Patient')

# --- 1. Master Data ---
vn, _ = Country.objects.get_or_create(name='Việt Nam', iso_code='VN')
p1, _ = Province.objects.get_or_create(name='TP. Hồ Chí Minh', code='79', country=vn)
p2, _ = Province.objects.get_or_create(name='Hà Nội', code='01', country=vn)
p3, _ = Province.objects.get_or_create(name='Đà Nẵng', code='48', country=vn)

s1, _ = Specialty.objects.get_or_create(name='Nội tổng quát', description='Khám nội khoa')
s2, _ = Specialty.objects.get_or_create(name='Nhi khoa', description='Khám cho trẻ em')
s3, _ = Specialty.objects.get_or_create(name='Sản phụ khoa', description='Chăm sóc mẹ và bé')
s4, _ = Specialty.objects.get_or_create(name='Tai Mũi Họng', description='Chuyên khoa TMH')
s5, _ = Specialty.objects.get_or_create(name='Da liễu', description='Điều trị bệnh ngoài da')

LabService.objects.get_or_create(name='Xét nghiệm máu', price=150000, description='XN tổng quát')
LabService.objects.get_or_create(name='Siêu âm bụng', price=250000, description='Siêu âm nội soi')
LabService.objects.get_or_create(name='X-Quang phổi', price=200000, description='Chụp phim phổi')
LabService.objects.get_or_create(name='Xét nghiệm nước tiểu', price=100000, description='XN nước tiểu')

# --- 2. Tài khoản (5 Bác sĩ + 15 Bệnh nhân = 20 Tài khoản) ---
specialties = [s1, s2, s3, s4, s5]

# Tạo 5 Bác sĩ
for i in range(1, 6):
    username = f'doctor{i}'
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, password='password123', role='DOCTOR')
        Profile.objects.create(user=u, name=f'Bác sĩ {i}', phone=f'091234500{i}', gender='Nam', dob='1980-01-01', province=p1, street_address='Clinic')
        Doctor.objects.create(user=u, specialty=specialties[i-1], experience=i+5, summary=f'Bác sĩ chuyên khoa {specialties[i-1].name}')

# Tạo 14 Bệnh nhân (cộng 1 Admin và 5 Bác sĩ là đủ 20)
for i in range(1, 15):
    username = f'patient{i}'
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, password='password123', role='PATIENT')
        Profile.objects.create(user=u, name=f'Bệnh nhân {i}', phone=f'03888880{i:02d}', gender='Nữ', dob='2000-01-01', province=p2, street_address='Home')
        Patient.objects.create(user=u, blood_type='O', height=165.5, weight=55.0, emergency_contact_name='Người thân', emergency_contact_phone='0900000000')

# --- 3. Dược phẩm ---
Medicine.objects.get_or_create(name='Panadol 500mg', unit='Vien', effect='Giảm đau', current_selling_price=2000)
Medicine.objects.get_or_create(name='Amoxicillin', unit='Vien', effect='Kháng sinh', current_selling_price=5000)
Medicine.objects.get_or_create(name='Hapacol', unit='Goi', effect='Hạ sốt cho trẻ', current_selling_price=3000)
Medicine.objects.get_or_create(name='Berberin', unit='Vien', effect='Tiêu hóa', current_selling_price=1000)
Medicine.objects.get_or_create(name='Vitamin C 500mg', unit='Vien', effect='Bổ sung vitamin', current_selling_price=1500)
Medicine.objects.get_or_create(name='Efferalgan', unit='Vien', effect='Giảm đau sủi', current_selling_price=4000)
Medicine.objects.get_or_create(name='Augmentin', unit='Vien', effect='Kháng sinh mạnh', current_selling_price=15000)
Medicine.objects.get_or_create(name='Decolgen', unit='Vien', effect='Trị cảm cúm', current_selling_price=2500)

print(">>> ĐÃ CHÈN DỮ LIỆU CỨNG THÀNH CÔNG (20 ACCOUNTS + MASTER DATA)")
EOF

echo "=== 5. Chạy server Django ==="
python manage.py runserver