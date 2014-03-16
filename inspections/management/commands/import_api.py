import pprint
import logging
import time
import requests

from django.core.management.base import BaseCommand

from inspections.models import Establishment, Inspection, Violation
from inspections.forms import EstablishmentForm, InspectionForm, ViolationForm


logger = logging.getLogger(__name__)


class DurhamAPI(object):
    url = "http://data.dconc.gov/ResturantData.aspx"

    def __init__(self, *args, **kwargs):
        self.params = kwargs

    def json(self):
        self.request = requests.get(self.url, params=self.params)
        logger.info("Requested {}".format(self.request.url))
        return self.request.json()


class Command(BaseCommand):
    """Import Durham inspections data from CSV files"""

    def import_api(self, json, Model, Form):
        objects = []
        start_time = time.time()
        for index, raw_row in enumerate(json):
            # create new row with matching field names
            row = {}
            for key, val in raw_row.items():
                new_key = key.lower().replace(' ', '_').replace('?', '')
                row[new_key] = val
            form = Form(dict(row))
            if not form.is_valid():
                errors = {'model': Model._meta.object_name,
                          'errors': dict(form.errors.items()),
                          'cleaned_data': form.cleaned_data,
                          'row': row}
                logger.error(pprint.pformat(errors, indent=4))
                continue
            objects.append(form.save())
            if index % 20 == 0:
                elapsed_time = time.time() - start_time
                msg = "{} ID: {} ({s:.2f} records/sec)".format(Model._meta.object_name, row['id'], s=len(objects)/elapsed_time)
                logger.debug(msg)
                start_time = time.time()
                objects = []

    def handle(self, *args, **options):
        self.import_api(DurhamAPI(est_type=1).json(),
                        Establishment, EstablishmentForm)
        for e in Establishment.objects.all():
            logger.debug(str(e))
            request = DurhamAPI(table="inspections", est_id=e.id)
            self.import_api(request.json(), Inspection, InspectionForm)
        # if not args:
        #     args = ['Establishment', 'Inspection', 'Violation']
        # for name in args:
        #     if name == 'Establishment':
        #         Model = Establishment
        #         Form = EstablishmentForm
        #     elif name == 'Inspection':
        #         Model = Inspection
        #         Form = InspectionForm
        #     elif name == 'Violation':
        #         Model = Violation
        #         Form = ViolationForm
        #     else:
        #         self.stdout.write("Invalid name: {}".format(name))
        #         continue
        #     self.import_api(name, Model, Form)
