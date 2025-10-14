from django.contrib import admin
from .models import Drug, Manufacturer, Generic, DosageForm

# Register your models here.
class DrugAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'dosage_form', 'manufacturer')
    search_fields = ('brand_name', 'generic__name', 'strength', 'dosage_form__description', 'manufacturer__name')
    list_filter = ('generic', 'dosage_form', 'manufacturer')

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GenericAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DosageFormAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

admin.site.register(Drug, DrugAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Generic, GenericAdmin)
admin.site.register(DosageForm, DosageFormAdmin)


