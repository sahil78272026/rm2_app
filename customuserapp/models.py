from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class FlatNumber(models.Model):
    flat_no = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return self.flat_no
class CustomUserModel(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    mobile = models.IntegerField(null=True)
    flat_no = models.ForeignKey(FlatNumber, max_length=10, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

class Visitor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    flat_no = models.ForeignKey(FlatNumber, max_length=10, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name





