# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 22:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent_treasures', '0002_auto_20180424_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='treasure',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]