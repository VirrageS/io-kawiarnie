# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 18:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0003_auto_20160521_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fullexpense',
            old_name='sum',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='fullexpense',
            old_name='report',
            new_name='cash_report',
        ),
    ]
