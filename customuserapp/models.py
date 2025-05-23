from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser

# Create your models here.

class FlatNumber(models.Model):
    flat_no = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self) -> str:
        return self.flat_no
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError("Mobile number is required")
        user = self.model(mobile=mobile, **extra_fields)
        if password:  # <-- only set if provided
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError("Mobile number is required")
        user = self.model(mobile=mobile, **extra_fields)
        if password:  # <-- only set if provided
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('resident', 'Resident'),
        ('guard', 'Guard'),
    )

    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    mobile = models.CharField(max_length=15, unique=True)  # use as login field
    flat_no = models.ForeignKey('FlatNumber', on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []  # nothing else is required

    def __str__(self):
        return self.mobile

class Visitor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    flat_no = models.ForeignKey(FlatNumber, max_length=10, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name





