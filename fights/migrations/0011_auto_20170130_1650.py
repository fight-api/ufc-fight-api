# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-30 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fights', '0010_auto_20170124_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='sherdog_url',
            new_name='sh_url',
        ),
        migrations.RenameField(
            model_name='fighter',
            old_name='sherdog_url',
            new_name='sh_url',
        ),
    ]