# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 23:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0006_auto_20161118_2311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tip',
            old_name='venueid',
            new_name='vid',
        ),
    ]
