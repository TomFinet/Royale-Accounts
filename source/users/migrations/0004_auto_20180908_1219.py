# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-08 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180908_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestEmailManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='guestemail',
            name='update',
        ),
    ]