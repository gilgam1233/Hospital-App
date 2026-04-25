from django.contrib import admin

class HospitalAdminSite(admin.AdminSite):
    site_header = "Hệ thống Quản lý Bệnh viện 2026"
    site_title = "Hospital Admin Portal"
    index_title = "Chào mừng đến với trang quản trị"

hospital_admin_site = HospitalAdminSite(name='hospital_admin')