# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_kaspi_1', '0002_auto_20161116_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('vid', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('text', models.TextField()),
            ],
        ),
    ]
