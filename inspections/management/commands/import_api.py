import pprint
import logging
import time
import requests
import io
import csv
import copy

from django.core.management.base import BaseCommand

from inspections.models import Establishment, Inspection, Violation
from inspections.forms import EstablishmentForm, InspectionForm, ViolationForm


logger = logging.getLogger(__name__)


class DurhamAPI(object):
    url = "http://data.dconc.gov/ResturantData.aspx"
    params = {'count': 200,
              'format': 'csv',
              'status': 'ACTIVE'}

    def get(self, *args, **kwargs):
        params = self.params.copy()
        params.update(kwargs)
        page = 1
        while True:
            params['page'] = page
            request = requests.get(self.url, params=params)
            logger.info("Requested {}".format(request.url))
            rows = list(csv.DictReader(io.StringIO(request.text)))
            if not rows:
                logger.info('No more data')
                return
            for row in rows:
                yield row
            page += 1


class Command(BaseCommand):
    """Import Durham inspections data from CSV files"""

    def import_api(self, data, Model, Form):
        objects = []
        start_time = time.time()
        for index, raw_row in enumerate(data):
            # create new row with matching field names
            row = {'external_id': raw_row['ID'],
                   'state_id': raw_row['State_Id'],
                   'name': raw_row['Premise_Name'],
                   'type': raw_row['Est_Type'],
                   'address': raw_row['Premise_Address1'],
                   'city': 'Durham',
                   'county': 'Durham',
                   'state': 'NC',
                   'postal_code': raw_row['Premise_Zip'],
                   'phone_number': raw_row['Premise_Phone'],
                   'opening_date': raw_row['Opening_Date'],
                   'update_date': raw_row['Update_Date'],
                   'status': raw_row['Status'],
                   'lat': raw_row['Lat'],
                   'lon': raw_row['Lon']}
            instance = None
            try:
                instance = Model.objects.get(external_id=row['external_id'],
                                             county=row['county'])
            except Model.DoesNotExist:
                pass
            form = Form(dict(row), instance=instance)
            if not form.is_valid():
                errors = {'model': Model._meta.object_name,
                          'errors': dict(form.errors.items()),
                          'cleaned_data': form.cleaned_data,
                          'raw_row': raw_row,
                          'row': row}
                logger.error(pprint.pformat(errors, indent=4))
                continue
            objects.append(form.save())
            if index % 20 == 0:
                elapsed_time = time.time() - start_time
                msg = "{} ID: {} ({s:.2f} records/sec)".format(Model._meta.object_name, row['external_id'], s=len(objects)/elapsed_time)
                logger.debug(msg)
                start_time = time.time()
                objects = []

    def handle(self, *args, **options):
        self.import_api(DurhamAPI().get(table="establishments", est_type=1),
                        Establishment, EstablishmentForm)
        # for e in Establishment.objects.all():
        #     request = DurhamAPI(table="inspections", est_id=e.id)
        #     self.import_api(request.json(), Inspection, InspectionForm)
        # for i in Inspection.objects.all():
        #     request = DurhamAPI(table="violations", inspection_id=i.id)
        #     self.import_api(request.json(), Violation, ViolationForm)
