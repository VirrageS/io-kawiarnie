# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-19 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stencils', '0005_auto_20160619_1032'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stencil',
            unique_together=set([('name', 'caffe')]),
        ),
    ]
