# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='vid',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]