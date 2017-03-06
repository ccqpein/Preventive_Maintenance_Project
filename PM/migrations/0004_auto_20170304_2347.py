# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0003_auto_20170222_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment_tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_name', models.CharField(max_length=100)),
                ('tool_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='name',
            new_name='eq_name',
        ),
        migrations.AddField(
            model_name='equipment',
            name='eq_type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
