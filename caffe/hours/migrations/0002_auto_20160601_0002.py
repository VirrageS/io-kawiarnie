# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-31 22:02
from __future__ import unicode_literals

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
        ),
        migrations.AlterModelOptions(
            name='workedhours',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'ordering': ('-date', '-end_time')},
        ),
        migrations.AddField(
            model_name='workedhours',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 31, 22, 1, 57, 830796, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workedhours',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 5, 31, 22, 2, 0, 555633, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workedhours',
            name='employee',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workedhours',
            name='position',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='hours.Position'),
        ),
    ]