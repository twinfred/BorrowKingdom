# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-25 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_treasures', '0004_auto_20180424_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasure',
            name='primary_img',
            field=models.ImageField(default='', upload_to=b''),
        ),
    ]
