# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-19 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stencils', '0004_stencil_caffe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stencil',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]