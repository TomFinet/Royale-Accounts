# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-19 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_account_player_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='clan_member_rank',
            field=models.CharField(choices=[('N', 'None'), ('M', 'Member'), ('E', 'Elder'), ('C', 'Co-Leader'), ('L', 'Leader')], max_length=2),
        ),
    ]
