# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-30 19:15
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='img_feature',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.main_image_upload_path),
        ),
    ]
