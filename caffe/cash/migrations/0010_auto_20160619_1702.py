# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-19 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0009_auto_20160615_2029'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set([('name', 'caffe')]),
        ),
        migrations.AlterUniqueTogether(
            name='expense',
            unique_together=set([('name', 'caffe')]),
        ),
    ]
