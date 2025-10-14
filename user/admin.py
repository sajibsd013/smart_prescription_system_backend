from django.contrib import admin
from .models import User, Patient, Doctor
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'phone', 'name')
    list_filter = (   'is_staff', 'is_active')
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('email', 'name', 'phone')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'is_active', 'is_staff')
        }),

    )

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'degree', 'reg_no', 'specialty', 'designation', 'hospital_name', 'created_at')
    search_fields = ('user__name', 'reg_no', 'specialty', 'degree', 'hospital_name')
    list_filter = ('specialty', 'hospital_name', 'created_at')
    readonly_fields = ('created_at', 'modified_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Doctor Information', {
            'fields': ('user', 'reg_no', 'degree', 'specialty', 'designation', 'hospital_name')
        }),
        ('System Information', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'blood_group', 'phone', 'created_at', 'modified_at')
    list_filter = ('gender', 'blood_group', 'created_at')
    search_fields = ('name', 'phone', 'email', 'address')
    readonly_fields = ('age', 'created_at', 'modified_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'dob', 'age', 'gender', 'blood_group')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Medical Information', {
            'fields': ('allergies',)
        }),
        ('System Information', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )

    def age(self, obj):
        return obj.age
    age.short_description = "Age"

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)

