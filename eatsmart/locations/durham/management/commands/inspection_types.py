import pprint

from django.core.management.base import BaseCommand

from eatsmart.locations.durham.api import DurhamAPI


class Command(BaseCommand):
    """Import saniation data from Durham County API"""

    def handle(self, *args, **options):
        types = {}
        for api in DurhamAPI().get(table="inspections", count=1000):
            if api['Insp_Type'] not in types:
                print(api['Insp_Type'], api['Type_description'])
                types[api['Insp_Type']] = api['Type_description'].strip()
        for api in DurhamAPI().get(table="inspections", count=1000,
                                   status='DELETED'):
            if api['Insp_Type'] not in types:
                print(api['Insp_Type'], api['Type_description'])
                types[api['Insp_Type']] = api['Type_description'].strip()
        pprint.pprint(types)
