# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0023_auto_20160214_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='event',
            field=models.ForeignKey(blank=True, to='firstpick.Event', null=True),
        ),
    ]
