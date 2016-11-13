# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0005_auto_20161103_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='pretty_name',
            field=models.CharField(verbose_name='Pretty Name', max_length=255, blank=True),
        ),
    ]
