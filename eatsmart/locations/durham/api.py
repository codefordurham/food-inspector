import csv
import io
import logging
import requests

from django.db.models import Max

from eatsmart.locations.base import Importer
from eatsmart.locations.durham.forms import (EstablishmentForm, InspectionForm,
                                             ViolationForm)
from inspections.models import Establishment, Inspection, Violation


logger = logging.getLogger(__name__)


class DurhamAPI(object):
    "Access and auto-paginate restaurant data from data.dconc.gov"

    url = "http://data.dconc.gov/ResturantData.aspx"
    params = {'count': 200,
              'format': 'csv',
              'status': 'ACTIVE'}

    def get(self, *args, **kwargs):
        "Request data and increment page number until response is empty"
        params = self.params.copy()
        params.update(kwargs)
        page = 1
        while True:
            params['page'] = page
            request = requests.get(self.url, params=params)
            logger.info("Requested {}".format(request.url))
            rows = list(csv.DictReader(io.StringIO(request.text)))
            if not rows:
                logger.debug('No more data')
                return
            for row in rows:
                yield row
            page += 1


class EstablishmentImporter(Importer):
    "Import Durham establishments"
    Model = Establishment
    Form = EstablishmentForm
    ColumnList = ['ID', 'State_Id', 'Premise_Name',
                  'Est_Type', 'Premise_Address1',
                  'Premise_Zip', 'Premise_City',
                  'Premise_Phone', 'Opening_Date',
                  'Update_Date', 'Status',
                  'Lat', 'Lon']
    LastDate = Model.objects.filter(county='Durham')
    LastDate = LastDate.aggregate(Max('update_date'))['update_date__max']

    def run(self, limit_set=False):
        "Fetch all Durham County establishments"
        api_kwargs = {'table': "establishments", 'est_type': 1,
                      'columns': ','.join(self.ColumnList)}
        if (limit_set):
            api_kwargs['Update_Date__gt'] = self.LastDate.strftime('%m/%d/%Y')
        self.fetch(DurhamAPI().get(**api_kwargs))

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
                'city': api['Premise_City'],
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
    "Import Durham inspections"

    Model = Inspection
    Form = InspectionForm
    ColumnList = ['Id', 'Insp_Date',
                  'Insp_Type', 'Score_SUM',
                  'Comments', 'Update_Date']
    LastDate = Model.objects.filter(establishment__county='Durham')
    LastDate = LastDate.aggregate(Max('update_date'))['update_date__max']

    def run(self, limit_set=False):
        "Fetch inspections for all Durham County establishments"
        api_kwargs = {'table': "inspections",
                      'columns': ','.join(self.ColumnList)}
        if (limit_set):
            api_kwargs['Update_Date__gt'] = self.LastDate.strftime('%m/%d/%Y')
        for est in Establishment.objects.filter(county='Durham'):
            # Only fetch inspections for establishments in our database
            api_kwargs['est_id'] = est.external_id
            self.fetch(DurhamAPI().get(**api_kwargs), establishment=est)

    def get_instance(self, data, establishment):
        "Instance exists if we have external_id for the given establishment"
        return self.Model.objects.get(external_id=data['external_id'],
                                      establishment=establishment)

    def get_last_inspection(self):
        "Retrieve the last inspection date"
        return self.LastDate

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
    "Import Durham violations"

    Model = Violation
    Form = ViolationForm
    ColumnList = ['Id', 'Item', 'Comments']

    def run(self, last_insp_date=None):
        "Fetch violations for all Durham County inspections"
        if (last_insp_date):
            inspections = Inspection.objects.filter(
                establishment__county='Durham',
                update_date__gt=last_insp_date)
        else:
            inspections = Inspection.objects.filter(
                establishment__county='Durham')
        api_kwargs = {'table': "violations",
                      'columns': ','.join(self.ColumnList)}
        for insp in inspections.select_related('establishment'):
            # Only fetch violations for inspections in our database
            api_kwargs['inspection_id'] = insp.external_id
            self.fetch(DurhamAPI().get(**api_kwargs), inspection=insp)

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
