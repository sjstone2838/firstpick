# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstpick', '0008_sportprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportprofile',
            name='active',
            field=models.CharField(choices=[(b'Yes', b'Yes'), (b'No', b'No')], default=b'Yes', max_length=100),
        ),
    ]
