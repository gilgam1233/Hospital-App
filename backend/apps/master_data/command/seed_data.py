import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.apps import apps
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Chèn dữ liệu mẫu cho hệ thống Polyclinic'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- ĐANG BẮT ĐẦU SEED DỮ LIỆU ---'))

        # 1. SEED MASTER DATA
        Country = apps.get_model('master_data', 'Country')
        vn, _ = Country.objects.get_or_create(name='Việt Nam', iso_code='VN')

        Province = apps.get_model('master_data', 'Province')
        hcm, _ = Province.objects.get_or_create(name='TP. Hồ Chí Minh', code='79', country=vn)
        hn, _ = Province.objects.get_or_create(name='Hà Nội', code='01', country=vn)
        dn, _ = Province.objects.get_or_create(name='Đà Nẵng', code='48', country=vn)

        Specialty = apps.get_model('master_data', 'Specialty')
        specialties = ['Nội tổng quát', 'Nhi khoa', 'Sản phụ khoa', 'Tai Mũi Họng', 'Da liễu']
        specialty_objs = []
        for s_name in specialties:
            s, _ = Specialty.objects.get_or_create(name=s_name, description=f'Chuyên khoa {s_name} chất lượng cao')
            specialty_objs.append(s)

        LabService = apps.get_model('master_data', 'LabService')
        lab_list = [('Xét nghiệm máu', 150000), ('Siêu âm bụng', 250000), ('X-Quang phổi', 200000), ('Xét nghiệm nước tiểu', 100000)]
        for name, price in lab_list:
            LabService.objects.get_or_create(name=name, description=f'Dịch vụ {name}', price=price)

        # 2. SEED ACCOUNTS (20 USERS)
        Profile = apps.get_model('accounts', 'Profile')
        Doctor = apps.get_model('accounts', 'Doctor')
        Patient = apps.get_model('accounts', 'Patient')

        # Tạo 1 Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@hospital.com', 'admin123', role='ADMIN')
            Profile.objects.create(user=admin, name="Tổng quản trị", gender="Nam", phone="0901234567", dob="1990-01-01", street_address="Hospital Center")

        # Tạo 5 Bác sĩ
        for i in range(1, 6):
            username = f'doctor{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password123', role='DOCTOR')
                Profile.objects.create(user=user, name=f'Bác sĩ {i}', gender=random.choice(['Nam', 'Nữ']), phone=f'091234500{i}', dob="1980-05-20", province=hcm)
                Doctor.objects.create(user=user, specialty=random.choice(specialty_objs), summary="Chuyên gia đầu ngành", experience=random.randint(5, 20))

        # Tạo 14 Bệnh nhân
        for i in range(1, 15):
            username = f'patient{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password123', role='PATIENT')
                Profile.objects.create(user=user, name=f'Bệnh nhân {i}', gender=random.choice(['Nam', 'Nữ']), phone=f'03888880{i:02d}', dob="2000-10-10", province=random.choice([hcm, hn, dn]))
                Patient.objects.create(user=user, blood_type=random.choice(['A', 'B', 'O', 'AB']), height=170, weight=65, emergency_contact_name="Người thân", emergency_contact_phone="0999888777")

        # 3. SEED PHARMACY (Dược phẩm)
        Medicine = apps.get_model('pharmacy', 'Medicine')
        med_list = ['Panadol 500mg', 'Paracetamol', 'Amoxicillin', 'Decolgen', 'Hapacol', 'Augmentin', 'Berberin', 'Vitamin C']
        for m_name in med_list:
            Medicine.objects.get_or_create(name=m_name, unit='Vien', effect='Giảm đau, hạ sốt', current_selling_price=random.randint(1000, 5000))

        self.stdout.write(self.style.SUCCESS('--- SEED DỮ LIỆU HOÀN TẤT (20 Users + Danh mục) ---'))