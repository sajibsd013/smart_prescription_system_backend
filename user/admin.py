from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role','phone', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active')
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name','role','phone')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'is_active', 'is_staff')
        }),

    )



admin.site.register(User, UserAdmin)
