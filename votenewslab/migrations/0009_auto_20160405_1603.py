# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-05 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votenewslab', '0008_remove_voteregion_tactic_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='cand_region_id',
            field=models.CharField(max_length=100),
        ),
    ]
