# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-14 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nin2newslab', '0020_tablemodal_modal_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='html_type',
            field=models.CharField(default='vertical-text', max_length=20),
            preserve_default=False,
        ),
    ]
