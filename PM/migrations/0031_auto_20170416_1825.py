# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0030_maintenancecontent_mc_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ord_date_comp',
            field=models.DateField(blank=True, null=True),
        ),
    ]
