# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_address', models.CharField(max_length=200, null=True, blank=True)),
                ('location_near_address', models.CharField(max_length=200, null=True, blank=True)),
                ('location_lat', models.DecimalField(null=True, max_digits=19, decimal_places=15, blank=True)),
                ('location_long', models.DecimalField(null=True, max_digits=19, decimal_places=15, blank=True)),
                ('location_note', models.CharField(max_length=200, null=True, blank=True)),
                ('location_number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptimizedLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_address', models.CharField(max_length=200, null=True, blank=True)),
                ('location_near_address', models.CharField(max_length=200, null=True, blank=True)),
                ('location_lat', models.DecimalField(null=True, max_digits=19, decimal_places=15, blank=True)),
                ('location_long', models.DecimalField(null=True, max_digits=19, decimal_places=15, blank=True)),
                ('location_note', models.CharField(max_length=200, null=True, blank=True)),
                ('location_number', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trip_title', models.CharField(max_length=100, null=True, blank=True)),
                ('total_distance', models.FloatField(default=0.0)),
                ('optimized_total_distance', models.FloatField(default=0.0)),
                ('optimized_total_time', models.CharField(max_length=30, null=True, blank=True)),
                ('total_time', models.CharField(max_length=30, null=True, blank=True)),
                ('trip_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='optimizedlocation',
            name='route',
            field=models.ForeignKey(related_name='optimized_route_locations', to='maps.Route'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='route',
            field=models.ForeignKey(related_name='route_locations', to='maps.Route'),
            preserve_default=True,
        ),
    ]
