# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-20 09:28
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_latest_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='latest',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest'),
        ),
    ]
