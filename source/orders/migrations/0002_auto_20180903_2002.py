# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-03 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Created', 'Created'), ('Paid', 'Paid'), ('Refunded', 'Refunded')], default='C', max_length=120),
        ),
    ]