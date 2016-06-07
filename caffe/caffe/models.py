"""Module with Caffe models."""

from django.db import models

from employees.models import Employee


class Caffe(models.Model):
    """Stores one cafe."""

    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    # CharField for extra characters like '-'
    postal_code = models.CharField(max_length=20)
    # CharFields in case house numbers like '1A'
    house_number = models.CharField(max_length=10)
    building_number = models.CharField(max_length=10, blank=True)
    created_on = models.TimeField(auto_now_add=True)
    creator = models.ForeignKey(Employee)

    def __str__(self):
        return '{}, {}'.format(self.name, self. city)
