# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0024_auto_20160214_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportprofile',
            name='rating_avg',
        ),
        migrations.RemoveField(
            model_name='sportprofile',
            name='rating_count',
        ),
    ]
