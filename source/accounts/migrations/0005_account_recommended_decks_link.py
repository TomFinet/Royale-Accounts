# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_accountimage_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='recommended_decks_link',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
