# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-08 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0020_auto_20170408_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='eq_next_main_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ord_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ord_date_comp',
            field=models.DateField(null=True),
        ),
    ]
