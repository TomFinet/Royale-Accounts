# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-19 14:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20180919_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='title',
        ),
    ]
