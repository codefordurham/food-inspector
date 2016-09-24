import time
import requests
from dateutil import parser

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from inspections.models import Establishment


class Command(BaseCommand):
    """Import saniation data from Durham County API"""
    restaurants_url = 'http://data.wake.opendata.arcgis.com/datasets/124c2187da8c41c59bde04fa67eb2872_0.geojson?where=&geometry={"xmin":-8992487.871106919,"ymin":4226590.155355151,"xmax":-8508182.859892275,"ymax":4318314.589297318,"spatialReference":{"wkid":102100}}'
    inspections_url = 'http://data.wake.opendata.arcgis.com/datasets/ebe3ae7f76954fad81411612d7c4fb17_1.geojson'
    violations_url = 'http://data.wake.opendata.arcgis.com/datasets/ebe3ae7f76954fad81411612d7c4fb17_1.geojson'

    def handle(self, *args, **options):
        # restaurants
        restaurants = self.get_county_data(self.restaurants_url)
        self.save_restaurants(restaurants)
        # inspections
        inspections = self.get_county_data(self.inspections_url)

        # violations
        violations = self.get_county_data(self.violations_url)

    def get_county_data(self, url):
        resp = requests.get(url)
        json_resp = resp.json()
        if 'features' in json_resp:
            return json_resp['features']
        time.sleep(30)  # wake queues up the response
        return self.get_county_data(url)

    def save_restaurants(self, restaurants):
        for restaurant in restaurants:
            properties = restaurant['properties']
            open_date = properties['RestaurantOpenDate']
            attributes = {
                'external_id': properties['OBJECTID'],
                'state_id': properties['HSISID'],
                'name': properties['Name'],
                # 'type': TODO: figure out a mappping that makes sense
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

