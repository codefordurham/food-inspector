import csv
import os
import io
import logging
import requests
import zipfile
import tempfile
import datetime
import time
import pprint


from eatsmart.locations.base import Importer
from eatsmart.locations.wake import forms
from inspections.models import Establishment, Inspection, Violation


logger = logging.getLogger(__name__)


class WakeCounty(object):

    url = "http://www.wakegov.com/data/Documents/WCRestaurantInspections.zip"

    def download_and_unzip_data(self, destination):
        logger.debug("Requesting {}".format(self.url))
        response = requests.get(self.url)
        archive = zipfile.ZipFile(io.BytesIO(response.content))
        logger.debug("Extracting archive into {}".format(str(destination)))
        archive.extractall(path=destination)

    def import_lives(self):
        with tempfile.TemporaryDirectory(prefix='wake') as destination:
            logger.debug("Created temp directory {}".format(destination))
            self.download_and_unzip_data(destination)
            businesses = os.path.join(destination, 'businesses.csv')
            # if os.path.exists(businesses):
            #     BusinessImporter().run(path=businesses)
            inspections = os.path.join(destination, 'inspections.csv')
            # Inspection.objects.filter(establishment__county='Wake').delete()
            # if os.path.exists(inspections):
            #     InspectionImporter().run(path=inspections)
            violations = os.path.join(destination, 'violations.csv')
            if os.path.exists(violations):
                ViolationImporter().run(path=violations)


class WakeCSVImporter(Importer):
    "Special importer to open CSV files using the Windows encoding"

    def run(self, path):
        logger.debug("Importing {}".format(path))
        with open(path, 'r', encoding='ISO-8859-1') as csv_file:
            reader = csv.DictReader(csv_file)
            self.fetch(reader)

    def fetch(self, data, **kwargs):
        "Primay import workflow with error handling"
        objects = []
        start_time = time.time()
        for index, api in enumerate(data):
            row = self.map_fields(api=api, **kwargs)
            form = self.Form(dict(row))
            if not form.is_valid():
                errors = {'model': self.Model._meta.object_name,
                          'errors': dict(form.errors.items()),
                          'cleaned_data': form.cleaned_data,
                          'api': api,
                          'row': row}
                logger.error(pprint.pformat(errors, indent=4))
                continue
            try:
                instance = self.get_instance(data=form.cleaned_data, **kwargs)
            except self.Model.DoesNotExist:
                # Instance doesn't exist, must be new
                instance = None
            if instance:
                form.instance = instance
            objects.append(form.save())
            if index % 20 == 0:
                elapsed_time = time.time() - start_time
                values = {'model': self.Model._meta.object_name,
                          'id': row.get('external_id', 'n/a'),
                          's': len(objects)/elapsed_time}
                msg = "{model} ID: {id} ({s:.2f} records/sec)".format(**values)
                logger.debug(msg)
                start_time = time.time()
                objects = []


class BusinessImporter(WakeCSVImporter):
    "Import Wake County, NC restaurants"

    Model = Establishment
    Form = forms.BusinessForm

    def get_instance(self, data):
        "Instance exists if we have external_id and it's within Wake County"
        return self.Model.objects.get(external_id=data['external_id'],
                                      county=data['county'])

    def map_fields(self, api):
        "Map CSV field names from Wake's data to our database schema"
        return {'external_id': api['business_id'],
                'name': api['name'],
                'type': 1,  # Restaurant
                'address': api['address'],
                'city': api['city'],
                'county': 'Wake',
                'state': 'NC',
                'postal_code': api['postal_code'],
                'phone_number': api['phone_number'],
                'lat': api['latitude'],
                'lon': api['longitude'],
                'status': 'active'}


class InspectionImporter(WakeCSVImporter):
    "Import Wake inspections"

    Model = Inspection
    Form = forms.InspectionForm

    def get_instance(self, data):
        "Inspections with same establishment, date, and type is existing"
        query = {
            'date': data['date'],
            'type': data['type'],
            'establishment': data['establishment'],
        }
        return self.Model.objects.get(**query)

    def map_fields(self, api):
        "Map CSV field names from Wake's data to our database schema"
        return {'establishment': api['business_id'],
                'date': api['date'],
                'type': api['type'],
                'score': api['score'],
                'description': api['description']}


class ViolationImporter(WakeCSVImporter):
    "Import Wake violations"

    Model = Violation
    Form = forms.ViolationForm

    def get_instance(self, data):
        "Instance exists if we have external_id for the given inspection"
        return self.Model.objects.get(date=data['date'],
                                      code=data['code'],
                                      inspection=data['inspection'])

    def map_fields(self, api):
        "Map CSV field names from Wake's data to our database schema"
        return {'establishment': api['business_id'],
                'date': api['date'],
                'code': api['code'],
                'description': api['description']}
