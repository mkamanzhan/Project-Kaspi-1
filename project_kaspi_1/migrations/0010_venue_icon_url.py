# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0009_auto_20161120_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='icon_url',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
