import os
import re
import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


PARENT_DIR = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
DATA_ROOT = os.path.join(PARENT_DIR, 'Durham-Data', 'Restaurants')
CSV_FILES = {
    'Establishment': os.path.join(DATA_ROOT, '2014-1-14-Establishments.csv'),
    'Inspection': os.path.join(DATA_ROOT, '2014-1-14-Inspections.csv'),
    'Violation': os.path.join(DATA_ROOT, '2014-1-14-Violations.csv'),
}
FIELD_MAP = {
    # establishments
    'ID': 'models.IntegerField(primary_key=True)',
    'County': 'models.IntegerField()',
    'Est_Type': 'models.IntegerField()',
    'Territory': 'models.IntegerField()',
    'State_Id': 'models.BigIntegerField()',
    'Prev_State_Id': 'models.BigIntegerField()',
    'Pay_Fee_Id': 'models.CharField(max_length=255, blank=True)',
    'Permit_Condition_Id': 'models.CharField(max_length=255, blank=True)',
    'Roster_Id': 'models.CharField(max_length=255, blank=True)',
    'Comments': 'models.TextField(blank=True)',
    'Permit_Conditions': 'models.TextField(blank=True)',
    'Lat': 'models.DecimalField(max_digits=17, decimal_places=15, null=True)',
    'Lon': 'models.DecimalField(max_digits=17, decimal_places=15, null=True)',
    # inspections
    'Id': 'models.IntegerField(primary_key=True)',
    'Est Id': 'models.ForeignKey("Establishment")',
    'Comment Sheet Id': 'models.CharField(max_length=255, blank=True)',
    'Followup Id': 'models.CharField(max_length=255, blank=True)',
    'State Id': 'models.BigIntegerField()',
    # violations
    'Inspection Id': 'models.ForeignKey("Inspection")',
    'Item': 'models.IntegerField()',
    'Weight SUM': 'models.FloatField()'
}


class Command(BaseCommand):
    """Inspect CSV file and build Django model stub"""

    def parse_field(self, table_name, field_name):
        django_field = None
        if field_name in FIELD_MAP:
            django_field = FIELD_MAP[field_name]
        # ignore dates split into columns
        if re.search("(Day|Month|Quarter|Year)$", field_name):
            return None
        # fields ending with _Date should be DateTimeField
        if not django_field and re.search("Date$", field_name):
            django_field = "models.DateTimeField(null=True)"
        # fields ending with _Id should be IntegerFields
        if not django_field and re.search("Id$", field_name):
            django_field = "models.IntegerField(null=True)"
        if not django_field:
            django_field = FIELD_MAP.get(field_name,
                                         "models.CharField(max_length=255, blank=True)")
        field = field_name.lower()
        field = field.replace(' ', '_')
        field = field.replace('?', '')
        return "    {} = {}".format(field, django_field)

    def handle(self, *args, **options):
        for table_name, path in CSV_FILES.items():
            self.stdout.write("\nclass {}(models.Model):".format(table_name))
            reader = csv.DictReader(open(CSV_FILES[table_name]))
            for field_name in reader.fieldnames:
                field = self.parse_field(table_name, field_name)
                if field:
                    self.stdout.write(field)
