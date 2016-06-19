# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-19 13:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caffe', '0004_auto_20160619_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caffe',
            name='creator',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_caffe', to=settings.AUTH_USER_MODEL),
        ),
    ]
