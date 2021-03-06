# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0009_auto_20170328_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='cl_cirnapmpbgcomment',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='cl_epilw',
            field=models.CharField(default='Yes', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='cl_fpilw',
            field=models.CharField(default='Yes', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='cl_fptsw',
            field=models.CharField(default='Yes', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checklist',
            name='cl_checkbox',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='cl_cirnapmpbg',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='cl_eptsw',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='cl_grbblw',
            field=models.CharField(max_length=20),
        ),
    ]
