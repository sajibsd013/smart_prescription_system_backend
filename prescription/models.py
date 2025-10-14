from django.db import models
from user.models import Patient, Doctor
from django.contrib.auth import get_user_model
User = get_user_model()

STATUS_CHOICES = [
    ('active', 'Active'),
    ('revoked', 'Revoked'),
]

MEDICATION_TYPES = [
    ('tablet', 'Tablet'),
    ('capsule', 'Capsule'),
    ('syrup', 'Syrup'),
    ('injection', 'Injection'),
    ('ointment', 'Ointment'),
    ('cream', 'Cream'),
    ('drops', 'Drops'),
    ('spray', 'Spray'),
    ('other', 'Other'),
]


class Complaint(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text

class History(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text

class Examination(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text

class Diagnosis(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text


class Investigation(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text


class Advice(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text


class FollowUp(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')

    # JSON fields (each prescription can have multiple items)
    complaint = models.JSONField(default=list, blank=True)
    history = models.JSONField(default=list, blank=True)
    exam = models.JSONField(default=list, blank=True)
    diagnosis = models.JSONField(default=list, blank=True)
    investigations = models.JSONField(default=list, blank=True)
    advice = models.JSONField(default=list, blank=True)
    follow_up = models.JSONField(default=list, blank=True)
    medication = models.JSONField(default=list, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rx #{self.id} - {self.patient} by {self.doctor}"



class PrescriptionVersionHistory(models.Model):
    prescription =  models.ForeignKey(Prescription, null=True, blank=True, on_delete=models.SET_NULL)
    version_number = models.PositiveIntegerField(default=1)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()
    action_type = models.CharField(max_length=10)  # create, update, delete

    class Meta:
        ordering = ['-changed_at']


