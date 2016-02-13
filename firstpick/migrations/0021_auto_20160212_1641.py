# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0020_event_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(max_length=200, choices=[(b'completed', b'completed'), (b'cancelled', b'cancelled'), (b'occurring', b'occurring'), (b'upcoming', b'upcoming')]),
        ),
    ]
