# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0004_auto_20161024_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='establishment',
            name='contamination_deductions',
        ),
        migrations.RemoveField(
            model_name='establishment',
            name='cook_temp_deductions',
        ),
        migrations.RemoveField(
            model_name='establishment',
            name='hold_temp_deductions',
        ),
        migrations.RemoveField(
            model_name='establishment',
            name='hygeine_deductions',
        ),
        migrations.RemoveField(
            model_name='establishment',
            name='source_deductions',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='contamination_deductions',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='cook_temp_deductions',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='hold_temp_deductions',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='hygeine_deductions',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='source_deductions',
        ),
        migrations.AlterField(
            model_name='establishment',
            name='contamination_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Contamination Count'),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='cook_temp_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Cooking Temperature Count'),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='hold_temp_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Holding Temperature Count'),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='hygeine_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Hygeine Count'),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='source_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Unsafe Source Count'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='contamination_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Contamination Count'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='cook_temp_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Cooking Temperature Count'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='hold_temp_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Holding Temperature Count'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='hygeine_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Hygeine Count'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='source_count',
            field=models.SmallIntegerField(default=-1, blank=True, verbose_name='Unsafe Source Count'),
        ),
    ]
