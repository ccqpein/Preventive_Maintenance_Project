# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 18:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0006_auto_20170327_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': (('view_order', 'Can view orders'),)},
        ),
    ]
