import os
import csv
import pprint

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


PARENT_DIR = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
DATA_ROOT = os.path.join(PARENT_DIR, 'Durham-Data', 'Restaurants')
CSV_FILES = {
    'Establishment': os.path.join(DATA_ROOT, '2014-1-14-Establishments.csv'),
    'Inspection': os.path.join(DATA_ROOT, '2014-1-14-Inspections.csv'),
    'Violation': os.path.join(DATA_ROOT, '2014-1-14-Violations.csv'),
}


class Command(BaseCommand):
    """Pretty print first row of specified CSV file"""

    def handle(self, *args, **options):
        reader = csv.DictReader(open(CSV_FILES[args[0]]))
        for row in reader:
            pprint.pprint(row, indent=4)
            return
