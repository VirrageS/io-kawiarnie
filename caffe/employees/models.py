from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# class EmployeeManager(models.Manager):
#     def employees(self):
#         return Entry.objects.all()


class Employee(AbstractUser):
    """Employee model, extends AbstractUser fields."""

    telephone_number = models.CharField(max_length=20)
    favorite_coffee = models.CharField(max_length=50)
