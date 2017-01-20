# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-20 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fights', '0005_auto_20160620_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('organization', models.CharField(max_length=255)),
                ('date_string', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
    ]
