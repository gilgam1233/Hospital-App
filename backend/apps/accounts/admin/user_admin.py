from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ..models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    # Thêm role vào fieldsets để có thể sửa trong admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Phân quyền', {'fields': ('role',)}),
    )