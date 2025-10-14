from django.contrib import admin
from .models import (
    Complaint, History, Examination, Diagnosis, Investigation,
    Advice, FollowUp, Prescription, PrescriptionVersionHistory
)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_label', 'patient', 'doctor', 'status', 'created_at', 'modified_at')
    list_filter = ('status', 'created_at', 'doctor')
    search_fields = ('patient__user__name', 'doctor__user__name')
    readonly_fields = ('created_at', 'modified_at')

    def prescription_label(self, obj):
        return f"Rx #{obj.id}"
    prescription_label.short_description = 'Prescription ID'

# Register clinical section models with default admin
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    search_fields = ('text',)

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    search_fields = ('text',)


@admin.register(PrescriptionVersionHistory)
class PrescriptionVersionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'prescription',
        'version_number',
        'action_type',
        'changed_by',
        'changed_at'
    )
    list_filter = ('action_type', 'changed_at', 'prescription')
    search_fields = ('prescription', 'changed_by')
    readonly_fields = ('prescription', 'version_number', 'action_type', 'changed_by', 'ip_address', 'changed_at')
    ordering = ('-changed_at',)

    fieldsets = (
        (None, {
            'fields': ('prescription', 'version_number', 'action_type', 'changed_by', 'ip_address', 'changed_at')
        }),
        ('Data Snapshot', {
            'fields': ('changes',),
        }),
    )

    def has_add_permission(self, request):
        # Prevent manual addition from admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Optional: prevent deletion from admin
        return False

