import csv
import os
import pprint
import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from inspections.models import Establishment
from inspections.forms import EstablishmentForm


PARENT_DIR = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
DATA_ROOT = os.path.join(PARENT_DIR, 'Durham-Data', 'Restaurants')
CSV_FILES = {
    'Establishment': os.path.join(DATA_ROOT, '2014-1-14-Establishments.csv'),
    'Inspection': os.path.join(DATA_ROOT, '2014-1-14-Inspections.csv'),
    'Violation': os.path.join(DATA_ROOT, '2014-1-14-Violations.csv'),
}


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Pretty print first row of specified CSV file"""

    def handle(self, *args, **options):
        Establishment.objects.all().delete()
        establishments = []
        with open(CSV_FILES['Establishment'], encoding='latin-1') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [n.lower() for n in reader.fieldnames]
            start_time = time.time()
            for index, row in enumerate(reader):
                form = EstablishmentForm(dict(row))
                if not form.is_valid():
                    errors = dict(form.errors.items())
                    logger.error(pprint.pformat(row, indent=4))
                    logger.error(pprint.pformat(errors, indent=4))
                    continue
                establishments.append(form.save(commit=False))
                if index % 500 == 0:
                    Establishment.objects.bulk_create(establishments)
                    elapsed_time = time.time() - start_time
                    msg = "Establishment ID: {} ({s:.2f} records/sec)".format(row['id'], s=len(establishments)/elapsed_time)
                    self.stdout.write(msg)
                    logger.debug(msg)
                    start_time = time.time()
                    establishments = []
