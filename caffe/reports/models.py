from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Report(models.Model):
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Report created: {:%Y-%m-%d %H:%M} '.format(self.date)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class FullProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    report = models.ForeignKey('Report', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return '{0}, {1:g} {2}'.format(
            self.product,
            self.amount,
            self.product.unit
        )
