# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nin2newslab', '0007_auto_20160201_0656'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=20)),
                ('p_price', models.IntegerField(default=10000)),
            ],
        ),
    ]