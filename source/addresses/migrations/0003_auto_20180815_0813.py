# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-15 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20180815_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='billing_city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='billing_country',
            field=models.CharField(choices=[('UK', 'United Kingdom'), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', ''), ('', '')], default='', max_length=2),
        ),
    ]
