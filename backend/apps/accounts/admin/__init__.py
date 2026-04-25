from django.contrib import admin
from .user_admin import UserAdmin
from ..models import User, Doctor, Patient, Profile

admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Profile)