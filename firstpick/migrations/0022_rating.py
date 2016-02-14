# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstpick', '0021_auto_20160212_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(verbose_name=b'DateTime Created')),
                ('attended', models.CharField(max_length=200, choices=[(b'Yes', b'Yes'), (b'No', b'No'), (b'Unknown', b'Unknown')])),
                ('rating', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('event', models.ForeignKey(to='firstpick.Event')),
                ('player', models.ForeignKey(related_name='Player', to=settings.AUTH_USER_MODEL)),
                ('rater', models.ForeignKey(related_name='Rater', to=settings.AUTH_USER_MODEL)),
                ('sport', models.ForeignKey(to='firstpick.Sport')),
            ],
        ),
    ]
