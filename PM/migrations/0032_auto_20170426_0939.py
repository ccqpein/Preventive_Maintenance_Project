# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0031_auto_20170416_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='eq_main_comment',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]