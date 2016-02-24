# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('external_id', models.CharField(max_length=128, verbose_name='External ID')),
                ('state_id', models.BigIntegerField(verbose_name='State ID')),
                ('property_id', models.CharField(blank=True, verbose_name='Property ID', max_length=128)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('type', models.PositiveIntegerField(verbose_name='Type', choices=[(0, 'Unknown'), (1, 'Restaurant'), (2, 'Food Stand'), (3, 'Mobile Food'), (4, 'Push Cart'), (5, "Private School's Cafeteria"), (6, 'Educational Food Service'), (9, 'Elderly Nutrition'), (11, "Public School's Cafeteria"), (12, 'Elderly Nutrition'), (14, 'Limited Food'), (15, 'Commissary (Pushcarts/Mobile Food),'), (16, 'Institutional Food Service'), (20, 'Lodging'), (21, 'Bed & Breakfast Home'), (22, 'Summer Camp'), (23, 'Bed & Breakfast Inn'), (25, 'Primitive Experience Camp'), (26, 'Resident Camp'), (30, 'Meat Market'), (40, 'Rest/Nursing Home'), (41, 'Hospital'), (42, 'Child Care'), (43, 'Residential Care'), (44, 'School Building'), (45, 'Local Confinement'), (46, 'Private Boarding School/College'), (47, "Orphanage, Children's Home"), (48, 'Adult Day Care'), (49, 'Adult Day Service'), (50, 'Seasonal Swimming Pool'), (51, 'Seasonal Wading Pool'), (52, 'Seasonal Spa'), (53, 'Year-Round Swimming Pool'), (54, 'Year-Round Wading Pool'), (55, 'Year-Round Spa'), (61, 'Tattoo Artist'), (72, 'Summer Feeding Program'), (73, 'Temporary Food Establishment')], default=0)),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('county', models.CharField(max_length=64, verbose_name='County', db_index=True)),
                ('state', models.CharField(max_length=64, verbose_name='State')),
                ('postal_code', models.CharField(max_length=16, verbose_name='Postal Code')),
                ('phone_number', models.CharField(blank=True, verbose_name='Phone Number', max_length=64)),
                ('opening_date', models.DateTimeField(verbose_name='Opening Date')),
                ('update_date', models.DateTimeField(null=True, verbose_name='Update Date', db_index=True, blank=True)),
                ('status', models.CharField(max_length=32, verbose_name='Status', choices=[('deleted', 'Deleted'), ('active', 'Active')], default='active')),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, verbose_name='location', srid=4326, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('external_id', models.CharField(max_length=128, verbose_name='External ID')),
                ('date', models.DateTimeField(verbose_name='Date', db_index=True)),
                ('score', models.FloatField(null=True, verbose_name='Score', blank=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type', models.PositiveIntegerField(verbose_name='Type', choices=[(0, 'Unknown'), (1, 'Routine Inspection'), (2, 'Re-inspection'), (5, 'Permit'), (6, 'Visit'), (8, 'Name Change'), (9, 'Verification'), (10, 'Other'), (12, 'Status Change'), (13, 'Pre-opening Visit'), (31, 'Critical Violation Visit'), (32, 'Critical Violation Followup')], default=0)),
                ('update_date', models.DateTimeField(null=True, verbose_name='Update Date', db_index=True, blank=True)),
                ('establishment', models.ForeignKey(related_name='inspections', to='inspections.Establishment', verbose_name='Establishment')),
            ],
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('external_id', models.CharField(max_length=128, verbose_name='External ID')),
                ('date', models.DateTimeField(verbose_name='Date', db_index=True)),
                ('code', models.CharField(max_length=32, verbose_name='Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('update_date', models.DateTimeField(null=True, verbose_name='Update Date', db_index=True, blank=True)),
                ('establishment', models.ForeignKey(related_name='violations', to='inspections.Establishment', verbose_name='Establishment')),
                ('inspection', models.ForeignKey(null=True, related_name='violations', blank=True, verbose_name='Inspection', to='inspections.Inspection')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='establishment',
            unique_together=set([('external_id', 'county')]),
        ),
    ]
