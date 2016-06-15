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


class Report(models.Model):
    """Stores a single report created from selected FullProducts.

    Date of creation is set automatically.
    Currently logged in user is assigned to report as creator.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        'employees.Employee',
        null=True,
        blank=True,
        default=None
    )
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('-created_on',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.creator is not None:
            if self.caffe != self.creator.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia tworzącego powinna się zgadzać')
                )

        self.full_clean()
        super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} {}'.format(
            self.created_on,
            self.creator
        )


class Category(models.Model):
    """Stores the category of a product, e.g. cake, tea, sandwich.

    Intended to be created once and then to reuse it in future reports.
    """

    name = models.CharField(max_length=100)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two products with same name
        query = Category.objects.filter(name=self.name, caffe=self.caffe)
        if self.pk:
            query = query.exclude(pk=self.pk)

        if query.exists():
            raise ValidationError(
                _('Kategoria powinna mieć unikalną nazwę.')
            )

        super(Category, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Unit(models.Model):
    """Stores a type of unit used to count the amount of products.

    Intended to be created once and then to reuse it in future reports.
    """

    name = models.CharField(max_length=100)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two units with same name
        query = Unit.objects.filter(name=self.name, caffe=self.caffe)
        if self.pk:
            query = query.exclude(pk=self.pk)

        if query.exists():
            raise ValidationError(
                _('Jednostka powinna mieć unikalną nazwę.')
            )

        super(Unit, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(Unit, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    """Stores a specific product, e.g. brownie, earl grey, PB&J sandwich.

    Intended to be created once and then to reuse it in future reports.
    Unit specifies how the amount of product is counted.
    """

    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        # checks if there exists two products with same name
        query = Product.objects.filter(name=self.name, caffe=self.caffe)
        if self.pk:
            query = query.exclude(pk=self.pk)

        if query.exists():
            raise ValidationError(
                _('Jednostka powinna mieć unikalną nazwę.')
            )

        super(Product, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        if self.caffe != self.category.caffe:
            raise ValidationError(
                _('Kawiarnia i kawiarnia kategorii nie zgadza się.')
            )

        if self.caffe != self.unit.caffe:
            raise ValidationError(
                _('Kawiarnia i kawiarnia jednostki nie zgadza się.')
            )

        self.full_clean()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class FullProduct(models.Model):
    """Stores a product with its quantity.

    Intended to be used once, only in one report.
    """

    product = models.ForeignKey('Product')
    amount = models.FloatField(validators=[MinValueValidator(0)])
    report = models.ForeignKey(
        'Report',
        blank=True,
        null=True,
        related_name='full_products'
    )
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

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

        if self.report:
            if self.caffe != self.report.caffe:
                raise ValidationError(
                    _('Kawiarnia i kawiarnia raportu nie zgadza się.')
                )

        if self.caffe != self.product.caffe:
            raise ValidationError(
                _('Kawiarnia i kawiarnia produktu nie zgadza się.')
            )

        self.full_clean()
        super(FullProduct, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}, {1:g} {2}'.format(
            self.product,
            self.amount,
            self.product.unit
        )
