from django.contrib import admin

from .models import GlobalConfig, Platform


@admin.register(GlobalConfig)
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ("rule_name", "default_value")
    search_fields = ("rule_name",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
