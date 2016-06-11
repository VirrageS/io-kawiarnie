"""Defines all the classes needed to create a Report from scratch.

Report: a single document about the state of a cafe.
Category: a class of products sharing common characteristics.
Product: a single item in a cafe.
Unit: a measure of products.
FullProduct: a product with its quantity.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from caffe.models import Caffe
from employees.models import Employee


class Report(models.Model):
    """Stores a single report created from selected FullProducts.

    Date of creation is set automatically.
    Currently logged in user is assigned to report as creator.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        Employee, unique=False, null=True, blank=True, default=None
    )
    caffe = models.ForeignKey(Caffe, null=True, blank=False, default=None)

    class Meta:
        ordering = ('-created_on',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} {}'.format(
            self.created_on,
            self.creator
        )


class Category(models.Model):
    """Stores the category of a product, e.g. cake, tea, sandwich.

    Intended to be created once and then to reuse it in future reports.
    """

    name = models.CharField(max_length=100, unique=True,)
    caffe = models.ForeignKey(Caffe, null=True, blank=False, default=None)

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    """Stores a specific product, e.g. brownie, earl grey, PB&J sandwich.

    Intended to be created once and then to reuse it in future reports.
    Unit specifies how the amount of product is counted.
    """

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    caffe = models.ForeignKey(Caffe, null=True, blank=False, default=None)

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return '{}'.format(self.name)


class Unit(models.Model):
    """Stores a type of unit used to count the amount of products.

    Intended to be created once and then to reuse it in future reports.
    """

    name = models.CharField(max_length=100, unique=True)
    caffe = models.ForeignKey(Caffe, null=True, blank=False, default=None)

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return '{}'.format(self.name)


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
    caffe = models.ForeignKey(Caffe, null=True, blank=False, default=None)

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two same products
        full_products = []
        if self.report is not None:
            full_products = self.report.full_products.all()

        for full_product in full_products:
            if full_product.product == self.product:
                raise ValidationError(
                    _('Report should not contain two same products.')
                )

        super(FullProduct, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(FullProduct, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}, {1:g} {2}'.format(
            self.product,
            self.amount,
            self.product.unit
        )
