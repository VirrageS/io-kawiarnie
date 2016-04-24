from django.db import models

from reports.models import Category


class Stencil(models.Model):
    """Stores template of Report which can be used to create Reports in faster
    manner.

    Attributes:
        name (str): Name for given Stencil.
        description (Optional(str)): Description for Stencil which should
            describe why this Stencil exists.
        categories (List(Category)): Categories which are used in creating
            Report from this Stencil.
    """

    name = models.CharField(max_length=100, unique=True,)
    description = models.TextField(max_length=500, null=True, blank=True,)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return '{}'.format(self.name)
