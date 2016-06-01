# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-01 17:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0002_auto_20160601_0002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='workedhours',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'change_all'), 'ordering': ('-date', '-end_time')},
        ),
    ]
