# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0003_auto_20161014_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='contamination_count',
            field=models.PositiveSmallIntegerField(verbose_name='Contamination Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='contamination_deductions',
            field=models.DecimalField(verbose_name='Contamination Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='cook_temp_count',
            field=models.PositiveSmallIntegerField(verbose_name='Cooking Temperature Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='cook_temp_deductions',
            field=models.DecimalField(verbose_name='Cooking Temperature Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='hold_temp_count',
            field=models.PositiveSmallIntegerField(verbose_name='Holding Temperature Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='hold_temp_deductions',
            field=models.DecimalField(verbose_name='Holding Temperature Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='hygeine_count',
            field=models.PositiveSmallIntegerField(verbose_name='Hygeine Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='hygeine_deductions',
            field=models.DecimalField(verbose_name='Hygeine Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='source_count',
            field=models.PositiveSmallIntegerField(verbose_name='Unsafe Source Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='establishment',
            name='source_deductions',
            field=models.DecimalField(verbose_name='Unsafe Source Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='contamination_count',
            field=models.PositiveSmallIntegerField(verbose_name='Contamination Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='contamination_deductions',
            field=models.DecimalField(verbose_name='Contamination Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='cook_temp_count',
            field=models.PositiveSmallIntegerField(verbose_name='Cooking Temperature Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='cook_temp_deductions',
            field=models.DecimalField(verbose_name='Cooking Temperature Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='hold_temp_count',
            field=models.PositiveSmallIntegerField(verbose_name='Holding Temperature Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='hold_temp_deductions',
            field=models.DecimalField(verbose_name='Holding Temperature Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='hygeine_count',
            field=models.PositiveSmallIntegerField(verbose_name='Hygeine Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='hygeine_deductions',
            field=models.DecimalField(verbose_name='Hygeine Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='source_count',
            field=models.PositiveSmallIntegerField(verbose_name='Unsafe Source Count', blank=True, default=0),
        ),
        migrations.AddField(
            model_name='inspection',
            name='source_deductions',
            field=models.DecimalField(verbose_name='Unsafe Source Deductions', decimal_places=2, blank=True, max_digits=4, default=0),
        ),
    ]
