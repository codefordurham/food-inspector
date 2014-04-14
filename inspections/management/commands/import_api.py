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


class Importer(object):

    def fetch(self, data, **kwargs):
        objects = []
        start_time = time.time()
        for index, api in enumerate(data):
            row = self.map_fields(api=api, **kwargs)
            try:
                instance = self.get_instance(data=row, **kwargs)
            except self.Model.DoesNotExist:
                instance = None
            form = self.Form(dict(row), instance=instance)
            if not form.is_valid():
                errors = {'model': self.Model._meta.object_name,
                          'errors': dict(form.errors.items()),
                          'cleaned_data': form.cleaned_data,
                          'api': api,
                          'row': row}
                logger.error(pprint.pformat(errors, indent=4))
                continue
            objects.append(form.save())
            if index % 20 == 0:
                elapsed_time = time.time() - start_time
                msg = "{} ID: {} ({s:.2f} records/sec)".format(self.Model._meta.object_name, row['external_id'], s=len(objects)/elapsed_time)
                logger.debug(msg)
                start_time = time.time()
                objects = []


class EstablishmentImporter(Importer):
    Model = Establishment
    Form = EstablishmentForm

    def run(self):
        "Fetch all Durham County establishments"
        self.fetch(DurhamAPI().get(table="establishments", est_type=1))

    def get_instance(self, data):
        "Instance exists if we have external_id and it's within Durham County"
        return self.Model.objects.get(external_id=data['external_id'],
                                      county=data['county'])

    def map_fields(self, api):
        "Map CSV field names from Durham's API to our database schema"
        return {'external_id': api['ID'],
                'state_id': api['State_Id'],
                'name': api['Premise_Name'],
                'type': api['Est_Type'],
                'address': api['Premise_Address1'],
                'city': 'Durham',
                'county': 'Durham',
                'state': 'NC',
                'postal_code': api['Premise_Zip'],
                'phone_number': api['Premise_Phone'],
                'opening_date': api['Opening_Date'],
                'update_date': api['Update_Date'],
                'status': api['Status'],
                'lat': api['Lat'],
                'lon': api['Lon']}


class InspectionImporter(Importer):
    Model = Inspection
    Form = InspectionForm

    def run(self):
        "Fetch inspections for all Durham County establishments"
        for est in Establishment.objects.filter(county='Durham'):
            # Only fetch inspections for establishments in our database
            api = DurhamAPI().get(table="inspections", est_id=est.external_id)
            self.fetch(api, establishment=est)

    def get_instance(self, data, establishment):
        "Instance exists if we have external_id for the given establishment"
        return self.Model.objects.get(external_id=data['external_id'],
                                      establishment=establishment)

    def map_fields(self, api, establishment):
        "Map CSV field names from Durham's API to our database schema"
        return {'external_id': api['Id'],
                'establishment': establishment.id,
                'date': api['Insp_Date'],
                'type': api['Insp_Type'],
                'score': api['Score_SUM'],
                'description': api['Comments'],
                'update_date': api['Update_Date']}


class ViolationImporter(Importer):
    Model = Violation
    Form = ViolationForm

    def run(self):
        "Fetch violations for all Durham County inspections"
        inspections = Inspection.objects.filter(establishment__county='Durham')
        for insp in inspections.select_related('establishment'):
            # Only fetch violations for inspections in our database
            api = DurhamAPI().get(table="violations",
                                  inspection_id=insp.external_id)
            self.fetch(api, inspection=insp)

    def get_instance(self, data, inspection):
        "Instance exists if we have external_id for the given inspection"
        return self.Model.objects.get(external_id=data['external_id'],
                                      inspection=inspection)

    def map_fields(self, api, inspection):
        "Map CSV field names from Durham's API to our database schema"
        return {'external_id': api['Id'],
                'inspection': inspection.id,
                'establishment': inspection.establishment.id,
                'date': inspection.date,
                'code': api['Item'],
                'description': api['Comments'],
                'update_date': inspection.update_date}


class Command(BaseCommand):
    """Import saniation data from Durham County API"""

    def handle(self, *args, **options):
        # EstablishmentImporter().run()
        # InspectionImporter().run()
        ViolationImporter().run()
