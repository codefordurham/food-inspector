# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0002_establishment_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='violation',
            name='deduction_value',
            field=models.DecimalField(max_digits=4, verbose_name='Deduction Value', decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='violation',
            name='risk_factor',
            field=models.PositiveIntegerField(verbose_name='Risk Factor', default=0, choices=[(0, 'Unknown'), (1, 'Improper Holding Temperature'), (2, 'Improper Cooking Temperature'), (3, 'Contaminated Equipment'), (4, 'Poor Hygiene'), (5, 'Food From Unsafe Sources'), (6, 'None')]),
        ),
    ]
