from django.db import models

from reports.models import Category

class Stencil(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{}'.format(self.name)
