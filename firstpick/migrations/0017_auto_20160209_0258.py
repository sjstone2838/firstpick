# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-09 02:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0016_auto_20160209_0256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='location_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='location_lat',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='location_lng',
            new_name='lng',
        ),
    ]