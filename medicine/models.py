from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Generic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class DosageForm(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description

class Drug(models.Model):
    brand_name = models.CharField(max_length=255)
    generic = models.ForeignKey(Generic, on_delete=models.CASCADE)
    strength = models.CharField(max_length=100)
    dosage_form = models.ForeignKey(DosageForm, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand_name} ({self.generic.name})"