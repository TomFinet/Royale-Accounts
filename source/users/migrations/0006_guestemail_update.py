# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-08 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_delete_guestemailmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestemail',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
