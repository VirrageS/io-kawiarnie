from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    """Employee model, extends AbstractUser fields."""

    telephone_number = models.CharField(max_length=20, blank=True)
    favorite_coffee = models.CharField(max_length=50, blank=True)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('last_name', 'first_name',)
        default_permissions = ('add', 'change', 'delete', 'view')
