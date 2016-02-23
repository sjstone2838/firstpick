# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0028_auto_20160223_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msg',
            name='msg_type',
            field=models.CharField(max_length=200, choices=[(b'New Event', b'New Event'), (b'RSVP Yes', b'RSVP Yes'), (b'RSVP No', b'RSVP No'), (b'Event Changed', b'Event Changed'), (b'Event Cancelled', b'Event Cancelled'), (b'Event Reminder', b'Event Reminder'), (b'Event Feedback', b'Event Feedback'), (b'Reset password', b'Reset password')]),
        ),
    ]
