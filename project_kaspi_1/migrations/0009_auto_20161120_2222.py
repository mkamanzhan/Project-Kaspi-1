# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 22:22
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0008_auto_20161119_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tip',
            name='vid',
        ),
        migrations.AddField(
            model_name='venue',
            name='tips',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=[], size=None),
        ),
        migrations.DeleteModel(
            name='Tip',
        ),
    ]