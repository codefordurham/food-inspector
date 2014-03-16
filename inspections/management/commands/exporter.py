import csv
import os
import pprint
import logging
import time
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from inspections.models import Establishment, Inspection, Violation
from inspections.forms import EstablishmentForm, InspectionForm, ViolationForm


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
    def exporter(self, name, Model, Form):
        with open(CSV_FILES[name],'w',newline='') as f:
            writer = csv.DictWriter(f,['Establishment.id','Establishment.property_id'])
            writer.writeheader()
            for E in Model.objects.filter(Q(est_type=1) & ~Q(property_id=0)):
                writer.writerow({'Establishment.id':str(E.id),'Establishment.property_id':str(E.property_id)})

    def handle(self, *args, **options):
        self.exporter('EstToProp',Establishment,EstablishmentForm)        
