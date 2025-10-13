from django.db import models

class MedicineDatabase(models.Model):
    manufacturer = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    strength = models.CharField(max_length=50)
    type = models.CharField(max_length=20, default='tablet')
    dosage = models.CharField(max_length=100)
    use_for = models.TextField(blank=True, null=True)
    dar = models.CharField(max_length=100, blank=True, null=True, verbose_name="Drug Approval Reference")

    def __str__(self):
        return f"{self.brand_name} ({self.generic_name})"