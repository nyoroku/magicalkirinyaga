# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-16 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]