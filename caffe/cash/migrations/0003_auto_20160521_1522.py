# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0002_auto_20160521_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
