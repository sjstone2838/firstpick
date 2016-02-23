# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0027_userprofile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='name',
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
    ]
