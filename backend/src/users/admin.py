from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Device


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Platform Context", {"fields": ("platform",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Platform Context", {"fields": ("platform", "email")}),
    )
    list_display = ("username", "email", "platform", "is_staff")
    list_filter = ("platform", "is_staff", "is_superuser")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "platform", "is_active", "last_seen")
    list_filter = ("platform", "is_active")
    search_fields = ("name", "user__email", "ip_address")
