# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0003_tip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tip',
            name='vid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_kaspi_1.Venue'),
        ),
    ]
