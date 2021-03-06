# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 04:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rent_treasures', '0013_auto_20180425_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2018, 4, 25, 21, 0, 53, 937000)),
        ),
        migrations.AlterField(
            model_name='order',
            name='treasure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='rent_treasures.Treasure'),
        ),
    ]
