from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserModel(AbstractUser):
    flat_no = models.CharField(max_length=10)

