# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-16 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_auto_20190716_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]