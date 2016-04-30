# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 20:58
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20160414_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullproduct',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='full_products', to='reports.Report'),
        ),
    ]
