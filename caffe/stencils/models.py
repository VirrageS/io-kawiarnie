from django.db import models

from reports.models import Category


class Stencil(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    description = models.TextField(max_length=500, null=True, blank=True,)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{}'.format(self.name)
