from django.db import models
from django.conf import settings


# Create your models here.

class UserType(models.Model):
    type = models.CharField(max_length=10)


class UserApp(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    type = models.ForeignKey(
        UserType, on_delete=models.CASCADE, null=False, blank=False)


class Appointment(models.Model):
    patient = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False, related_name="patients")
    veterinarian = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False, related_name="veterinarians+")
    appointment_date_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'''Appointment ID: {self.id} - Patient: {self.patient.name} - Date: {self.appointment_date_time.day}/{self.appointment_date_time.month} : {self.appointment_date_time.hour}'''


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False, related_name="patients+")
    veterinarian = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False, related_name="veterinarians")
    diagnosis = models.TextField()
    treatments = models.TextField()
    medications = models.TextField()
    vaccinations = models.TextField()
    surgeries = models.TextField()
    allergies = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

    def __str__(self):
        return f'Medical Record ID: {self.id} for {self.patient}'


class Invoice(models.Model):
    patient = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Document(models.Model):
    patient = models.ForeignKey(
        UserApp, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
