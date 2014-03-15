import csv
import pprint
import logging
import time
import requests

from django.core.management.base import BaseCommand

from inspections.models import Establishment, Inspection, Violation
from inspections.forms import EstablishmentForm, InspectionForm, ViolationForm


API_ENDPOINTS = {
    'Establishment': 'http://data.dconc.gov/ResturantData.aspx',
    'Inspection': 'http://data.dconc.gov/ResturantData.aspx?table=inspections',
    'Violation': 'http://data.dconc.gov/ResturantData.aspx',
}


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Import Durham inspections data from CSV files"""

    def import_api(self, name, Model, Form):
        Model.objects.all().delete()
        self.stdout.write("Requesting {}".format(API_ENDPOINTS[name]))
        r = requests.get(API_ENDPOINTS[name])
        self.stdout.write("Processing...")
        objects = []
        start_time = time.time()
        for index, raw_row in enumerate(r.json()):
            # create new row with matching field names
            row = {}
            for key, val in raw_row.items():
                new_key = key.lower().replace(' ', '_').replace('?', '')
                row[new_key] = val
            form = Form(dict(row))
            if not form.is_valid():
                errors = dict(form.errors.items())
                logger.error(pprint.pformat(row, indent=4))
                logger.error(pprint.pformat(form.cleaned_data, indent=4))
                logger.error(pprint.pformat(errors, indent=4))
                continue
            objects.append(form.save(commit=False))
            if index % 20 == 0:
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
            self.import_api(name, Model, Form)
