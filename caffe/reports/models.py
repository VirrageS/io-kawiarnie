from django.db import models


class Report(models.Model):
    date = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            )


class Product(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            )
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 )
    unit = models.ForeignKey('Unit',
                             on_delete=models.CASCADE,
                             )


class Unit(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            )


class FullProduct(models.Model):
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                )
    amount = models.PositiveIntegerField()
    report = models.ForeignKey('Report',
                               on_delete=models.CASCADE,
                               )