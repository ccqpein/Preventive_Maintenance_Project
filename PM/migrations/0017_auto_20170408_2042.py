# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-08 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0016_auto_20170404_2103'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CheckList',
        ),
        migrations.DeleteModel(
            name='SafetyCheck',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='eq_internal_part_num',
            field=models.CharField(max_length=100),
        ),
    ]
