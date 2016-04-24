from django.contrib.auth.models import AbstractUser
from django.db import models


# class EmployeeManager(models.Manager):
#     def employees(self):
#         return Entry.objects.all()


class Employee(AbstractUser):
    telephone_number = models.CharField(max_length=20)
