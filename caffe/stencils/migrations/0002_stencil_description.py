# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stencils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stencil',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]