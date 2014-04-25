import csv
import os
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from inspections.models import Establishment


PARENT_DIR = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
DATA_ROOT = os.path.join(PARENT_DIR, 'Durham-Data', 'Restaurants')
CSV_FILES = {
    'Establishment': os.path.join(DATA_ROOT, '2014-1-14-Establishments.csv'),
    'Inspection': os.path.join(DATA_ROOT, '2013-12-17-Inspections.csv'),
    'Violation': os.path.join(DATA_ROOT, '2013-12-17-Violations.csv'),
    'EstToProp': os.path.join(DATA_ROOT, 'establishments_propid.csv'),
}

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    """Import Durham inspections data from CSV files"""
    def importer(self, name, Model):
        with open(CSV_FILES[name], encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for m in Model.objects.filter(external_id=int(row['Establishment.id'])):
                    m.property_id = int(row['Establishment.property_id'])
                    m.save()

    def handle(self, *args, **options):
        self.importer('EstToProp', Establishment)
