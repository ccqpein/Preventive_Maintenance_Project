# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0027_order_ord_assign'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='eq_main_comment',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]