from django.contrib import admin
from .models import (
    Complaint, History, Examination, Diagnosis, Investigation,
    Advice, FollowUp, Medication, Prescription
)

# Inline classes for showing ManyToMany relationships in Prescription admin
class MedicationInline(admin.TabularInline):
    model = Prescription.medication.through
    extra = 0

class ComplaintInline(admin.TabularInline):
    model = Prescription.complaint.through
    extra = 0

class HistoryInline(admin.TabularInline):
    model = Prescription.history.through
    extra = 0

class ExaminationInline(admin.TabularInline):
    model = Prescription.exam.through
    extra = 0

class DiagnosisInline(admin.TabularInline):
    model = Prescription.diagnosis.through
    extra = 0

class InvestigationInline(admin.TabularInline):
    model = Prescription.investigations.through
    extra = 0

class AdviceInline(admin.TabularInline):
    model = Prescription.advice.through
    extra = 0

class FollowUpInline(admin.TabularInline):
    model = Prescription.follow_up.through
    extra = 0

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_label', 'patient', 'doctor', 'status', 'created_at', 'modified_at')
    list_filter = ('status', 'created_at', 'doctor')
    search_fields = ('patient__user__name', 'doctor__user__name')
    readonly_fields = ('created_at', 'modified_at')

    inlines = [
        MedicationInline,
        ComplaintInline,
        HistoryInline,
        ExaminationInline,
        DiagnosisInline,
        InvestigationInline,
        AdviceInline,
        FollowUpInline
    ]

    fieldsets = (
        ('Patient & Doctor Info', {
            'fields': ('patient', 'doctor')
        }),
        # ('Clinical Sections', {
        #     'fields': ('complaint', 'history', 'exam', 'diagnosis', 'investigations', 'advice', 'follow_up')
        # }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'modified_at')
        }),
    )

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

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'generic_name', 'strength', 'dosage', 'duration')
    search_fields = ('brand_name', 'generic_name')
    list_filter = ('generic_name',)
