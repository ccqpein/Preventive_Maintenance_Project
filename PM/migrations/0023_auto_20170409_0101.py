# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 01:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0022_maintenanceschedule_mc_next_main_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenanceschedule',
            old_name='mc_last_main_date',
            new_name='ms_last_main_date',
        ),
        migrations.RenameField(
            model_name='maintenanceschedule',
            old_name='mc_next_main_date',
            new_name='ms_next_main_date',
        ),
    ]
