import csv
import os
import pprint
import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from inspections.models import Establishment, Inspection, Violation
from inspections.forms import EstablishmentForm, InspectionForm, ViolationForm


PARENT_DIR = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
DATA_ROOT = os.path.join(PARENT_DIR, 'Durham-Data', 'Restaurants')
CSV_FILES = {
    'Establishment': os.path.join(DATA_ROOT, '2014-1-14-Establishments.csv'),
    'Inspection': os.path.join(DATA_ROOT, '2013-12-17-Inspections.csv'),
    'Violation': os.path.join(DATA_ROOT, '2013-12-17-Violations.csv'),
}


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Import Durham inspections data from CSV files"""

    def import_csv(self, name, Model, Form):
        Model.objects.all().delete()
        objects = []
        with open(CSV_FILES[name], encoding='latin-1') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [n.lower().replace(' ', '_').replace('?', '') for n in reader.fieldnames]
            start_time = time.time()
            for index, row in enumerate(reader):
                form = Form(dict(row))
                if not form.is_valid():
                    errors = dict(form.errors.items())
                    logger.error(pprint.pformat(row, indent=4))
                    logger.error(pprint.pformat(errors, indent=4))
                    continue
                objects.append(form.save(commit=False))
                if index % 500 == 0:
                    Model.objects.bulk_create(objects)
                    elapsed_time = time.time() - start_time
                    msg = "{} ID: {} ({s:.2f} records/sec)".format(name, row['id'], s=len(objects)/elapsed_time)
                    self.stdout.write(msg)
                    logger.debug(msg)
                    start_time = time.time()
                    objects = []

    def handle(self, *args, **options):
        if not args:
            args = ['Establishment', 'Inspection', 'Violation']
        for name in args:
            if name == 'Establishment':
                Model = Establishment
                Form = EstablishmentForm
            elif name == 'Inspection':
                Model = Inspection
                Form = InspectionForm
            elif name == 'Violation':
                Model = Violation
                Form = ViolationForm
            else:
                self.stdout.write("Invalid name: {}".format(name))
                continue
            self.import_csv(name, Model, Form)
