# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 02:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_treasures', '0012_order_return_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treasure',
            name='status',
        ),
        migrations.AlterField(
            model_name='order',
            name='return_date',
            field=models.DateField(default=datetime.datetime(2018, 4, 25, 19, 30, 49, 759000)),
        ),
    ]
