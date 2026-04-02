from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "name", "department", "year", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "name", "department")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("name", "department", "year")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "department", "year", "password1", "password2"),
        }),
    )

# Register your models here.
