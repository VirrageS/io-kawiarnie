from django.db import models

# class EmployeeManager(models.Manager):
#     def employees(self):
#         return Entry.objects.all()

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
