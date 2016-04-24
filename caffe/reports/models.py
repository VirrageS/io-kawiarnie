"""Defines all the classes needed to create a Report from scratch.

Report: a single document about the state of a cafe.
Category: a class of products sharing common characteristics.
Product: a single item in a cafe.
Unit: a measure of products.
FullProduct: a product with its quantity.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Report(models.Model):
    """Stores a single report created from selected FullProducts.

    Date of creation is set automatically.
    """
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} '.format(self.created_on)


@python_2_unicode_compatible
class Category(models.Model):
    """Stores the category of a product, e.g. cake, tea, sandwich.

    Intended to be created once and then to reuse it in future reports.
    """
    name = models.CharField(max_length=100, unique=True,)

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Product(models.Model):
    """Stores a specific product, e.g. brownie, earl grey, PB&J sandwich.

    Intended to be created once and then to reuse it in future reports.
    Unit specifies how the amount of product is counted.
    """
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Unit(models.Model):
    """Stores a type of unit used to count the amount of products.

    Intended to be created once and then to reuse it in future reports.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class FullProduct(models.Model):
    """Stores a product with its quantity.

    Intended to be used once, only in one report.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    report = models.ForeignKey(
        'Report',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='full_products'
    )

    def __str__(self):
        return '{0}, {1:g} {2}'.format(
            self.product,
            self.amount,
            self.product.unit
        )
