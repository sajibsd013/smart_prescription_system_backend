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

class Medication(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, default='tablet')
    strength = models.CharField(max_length=50)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.brand_name} ({self.dosage})"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')

    # Many-to-Many Fields (each prescription can have multiple items)
    complaint = models.ManyToManyField(Complaint, blank=True, related_name='prescriptions')
    history = models.ManyToManyField(History, blank=True, related_name='prescriptions')
    exam = models.ManyToManyField(Examination, blank=True, related_name='prescriptions')
    diagnosis = models.ManyToManyField(Diagnosis, blank=True, related_name='prescriptions')
    investigations = models.ManyToManyField(Investigation, blank=True, related_name='prescriptions')
    advice = models.ManyToManyField(Advice, blank=True, related_name='prescriptions')
    follow_up = models.ManyToManyField(FollowUp, blank=True, related_name='prescriptions')
    medication = models.ManyToManyField(Medication, related_name='prescriptions')


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rx #{self.id} - {self.patient} by {self.doctor}"




class PrescriptionVersionHistory(models.Model):
    object_id = models.PositiveIntegerField()
    version_number = models.PositiveIntegerField(default=1)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    changed_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
    change_type = models.CharField(max_length=10)  # create, update, delete

    class Meta:
        ordering = ['-changed_at']


