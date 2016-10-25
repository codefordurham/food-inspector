import time
import requests
from dateutil import parser

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from inspections.models import Establishment, Inspection, Violation


class Command(BaseCommand):
    """Import saniation data from Durham County API"""
    restaurants_url = 'http://data.wake.opendata.arcgis.com/datasets/124c2187da8c41c59bde04fa67eb2872_0.geojson?where=&geometry={"xmin":-8992487.871106919,"ymin":4226590.155355151,"xmax":-8508182.859892275,"ymax":4318314.589297318,"spatialReference":{"wkid":102100}}'
    inspections_url = 'http://data.wake.opendata.arcgis.com/datasets/ebe3ae7f76954fad81411612d7c4fb17_1.geojson'
    violations_url = 'http://data.wake.opendata.arcgis.com/datasets/9b04d0c39abd4e049cbd4656a0a04ba3_2.geojson'

    def handle(self, *args, **options):
        # restaurants
        restaurants = self.get_county_data(self.restaurants_url)
        self.save_restaurants(restaurants)
        # inspections
        inspections = self.get_county_data(self.inspections_url)
        self.save_inspections(inspections)
        # violations
        violations = self.get_county_data(self.violations_url)
        self.save_violations(violations)

    def get_county_data(self, url):
        resp = requests.get(url)
        json_resp = resp.json()
        if 'features' in json_resp:
            return json_resp['features']
        time.sleep(30)  # wake queues up the response
        return self.get_county_data(url)

    def get_establishment_type(self, wake_type):
        wake_type_dict = {
            'Meat Market': 30,
            'Private School Lunchrooms': 5,
            'Mobile Food Units': 3,
            'Limited Food Service': 14,
            'Restaurant': 1,
            'Elderly Nutrition Sites (catered)': 9,
            'Institutional Food Service': 16,
            'Public School Lunchrooms': 11,
            'Pushcarts': 4,
            'Food Stand': 2
            }
        try:
            return wake_type_dict[wake_type]
        except KeyError:
            return 0

    def save_restaurants(self, restaurants):
        for restaurant in restaurants:
            properties = restaurant['properties']
            open_date = properties['RestaurantOpenDate']
            attributes = {
                'external_id': properties['HSISID'],
                'state_id': properties['HSISID'],
                'name': properties['Name'],
                'type': self.get_establishment_type(properties['FacilityType']),
                'address': '{0} {1}'.format(properties['Address1'], properties['Address2']).rstrip(),
                'city': properties['City'],
                'county': 'Wake',
                'state': 'NC',
                'postal_code': properties['PostalCode'],
                'opening_date': parser.parse(open_date) if open_date else None,
                'location': Point(float(properties['X']), float(properties['Y']))
            }
            try:
                restaurant_obj = Establishment.objects.get(state_id=properties['HSISID'])
                print('Already in db')
            except Establishment.DoesNotExist:
                restaurant_obj = Establishment()
                print('New record')
            restaurant_obj.__dict__.update(**attributes)
            restaurant_obj.save()

    def get_inspection_type(self, inspection_type):
        inspection_type_dict = {
            'Inspection': 1,
            'Re-Inspection': 2
            }
        try:
            return inspection_type_dict[inspection_type]
        except KeyError:
            return 0

    def save_inspections(self, inspections):
        for inspection in inspections:
            properties = inspection['properties']
            try:
                establishment = Establishment.objects.get(state_id=int(properties['HSISID']))
            except:
                print('No Establishment with HSISID #' + properties['HSISID'])
                continue
            insp_date = properties['Date']
            attributes = {
                'establishment_id': establishment.id,
                'external_id': properties['OBJECTID'],
                'date': parser.parse(insp_date) if insp_date else None,
                'score': properties['Score'],
                'description': properties['Description'],
                'type': self.get_inspection_type(properties['Type'])
            }
            try:
                inspection_obj = Inspection.objects.get(establishment_id=establishment.id,
                                                        date=insp_date)
                print('Already in db')
            except Inspection.DoesNotExist:
                inspection_obj = Inspection()
                print('New record')
            inspection_obj.__dict__.update(**attributes)
            inspection_obj.save()

    def get_risk_factor_value(self, risk_factor):
        risk_factor_dict = {
            'Food from Unsafe Sources': 5,
            'Improper Holding': 1,
            'Food from Unsafe Source': 5,
            'Poor Personal Hygiene': 4,
            None: 6,
            'Contaminated Equipment': 3,
            'Inadequate Cook': 2
        }
        try:
            return risk_factor_dict[risk_factor]
        except KeyError:
            return 0

    def save_violations(self, violations):
        for violation in violations:
            properties = violation['properties']
            inspection_date = parser.parse(properties['InspectDate'])
            try:
                establishment = Establishment.objects.get(state_id=int(properties['HSISID']))
            except Establishment.DoesNotExist:
                print('No Establishment with HSISID #' + properties['HSISID'])
                continue
            except TypeError:
                if not properties['HSISID']:
                    print('Object #' + str(properties['OBJECTID']) + ' is NoneType')
                else:
                    print('Object #' + str(properties['OBJECTID']) + ' is  type' + str(type(properties['HSISID'])))
                continue
            try:
                inspection = Inspection.objects.get(establishment_id=establishment.id,
                                                    date=inspection_date)
            except Inspection.DoesNotExist:
                print('No Inspection for HSISID #' + properties['HSISID'] +
                      ' with date ' + str(inspection_date))
                continue
            attributes = {
                'establishment_id': establishment.id,
                'inspection_id': inspection.id,
                'external_id': properties['OBJECTID'],
                'date': inspection_date,
                'code': properties['ViolationCode'],
                'description': properties['shortdesc'],
                'risk_factor': self.get_risk_factor_value(properties['CDCRiskFactor']),
                'deduction_value': properties['pointValue']
            }
            try:
                violation_obj = Violation.objects.get(establishment_id=establishment.id,
                                                      date=inspection_date,
                                                      code=properties['ViolationCode'])
                print('ObjectID: ' + str(properties['OBJECTID']) + ' already in db')
            except Violation.DoesNotExist:
                violation_obj = Violation()
                print('New record')
            violation_obj.__dict__.update(**attributes)
            violation_obj.save()
