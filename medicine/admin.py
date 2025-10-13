from django.contrib import admin

from .models import MedicineDatabase

class MedicineDatabaseAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'generic_name', 'strength', 'type', 'manufacturer')
    search_fields = ('brand_name', 'generic_name', 'manufacturer')
    list_filter = ('type', 'manufacturer')
    ordering = ('brand_name',)

admin.site.register(MedicineDatabase, MedicineDatabaseAdmin)
