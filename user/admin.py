from django.contrib import admin
from .models import User, Patient, Doctor
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'phone', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'phone', 'name')
    list_filter = ('role',  'is_staff', 'is_active')
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('email', 'name', 'role','phone')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'is_active', 'is_staff')
        }),

    )

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user__name', 'specialty', 'reg_no', 'user__phone')
    search_fields = ('user__email', 'user__name', 'specialty', 'reg_no')
    list_filter = ('specialty',)
    ordering = ('-id',)


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user__name', 'dob', 'address', 'user__phone')
    search_fields = ('user__email', 'user__name', 'address')
    ordering = ('-id',)

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)

