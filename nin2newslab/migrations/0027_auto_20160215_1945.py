# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 19:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nin2newslab', '0026_auto_20160215_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchoice',
            old_name='urjson',
            new_name='json',
        ),
        migrations.RemoveField(
            model_name='userchoice',
            name='age',
        ),
    ]
