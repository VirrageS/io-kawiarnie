# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-21 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20160521_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('-created_on',)},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('name',)},
        ),
    ]
