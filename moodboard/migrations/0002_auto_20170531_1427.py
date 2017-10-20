# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='directory',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='userimage',
            name='tags',
            field=models.ManyToManyField(to='moodboard.Tag', blank=True),
        ),
    ]
