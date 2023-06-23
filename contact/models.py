from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    created_contact = models.DateTimeField(default=timezone.now)
