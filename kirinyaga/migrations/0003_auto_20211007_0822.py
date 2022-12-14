# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-10-07 05:22
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('kirinyaga', '0002_auto_20211005_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='stay',
            name='website',
            field=models.URLField(blank=True, help_text='If you do not have a website leave the field blank '),
        ),
        migrations.AlterField(
            model_name='place',
            name='website',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='stay',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Use +254 format', max_length=128, region=None),
        ),
    ]
