from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        if not email.endswith("@yourcollege.edu"):
            raise ValueError("Only @yourcollege.edu emails are allowed.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    YEAR_CHOICES = [(str(i), str(i)) for i in range(1, 5)]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=120)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "department", "year"]

    def __str__(self):
        return f"{self.name} ({self.email})"

# Create your models here.
