# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-05 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180903_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountimage',
            name='description',
            field=models.CharField(default='n', max_length=100),
            preserve_default=False,
        ),
    ]