# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-15 17:57
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caffe', '0001_initial'),
        ('cash', '0007_auto_20160526_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashreport',
            name='caffe',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='caffe.Caffe'),
        ),
        migrations.AddField(
            model_name='company',
            name='caffe',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='caffe.Caffe'),
        ),
        migrations.AddField(
            model_name='expense',
            name='caffe',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='caffe.Caffe'),
        ),
        migrations.AddField(
            model_name='fullexpense',
            name='caffe',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='caffe.Caffe'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
