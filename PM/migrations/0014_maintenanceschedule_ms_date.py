# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0013_auto_20170402_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceschedule',
            name='ms_date',
            field=models.DateField(auto_now=True),
        ),
    ]
