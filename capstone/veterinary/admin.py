from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Appointment)
admin.site.register(models.MedicalRecord)
admin.site.register(models.Invoice)
admin.site.register(models.InventoryItem)
admin.site.register(models.Document)
