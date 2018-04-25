# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rent_treasures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_token', models.CharField(default='Pending', max_length=255)),
                ('amount', models.PositiveIntegerField()),
                ('days', models.PositiveIntegerField()),
                ('pickup_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='rent_treasures.User')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='request_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='stripe_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='treasure',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='treasure',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rent_treasures.Treasure'),
        ),
    ]