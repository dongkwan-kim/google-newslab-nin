# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-05 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votenewslab', '0011_candidate_cand_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta',
            name='meta_title',
            field=models.CharField(max_length=40),
        ),
    ]
