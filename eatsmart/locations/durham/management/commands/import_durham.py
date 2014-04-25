from django.core.management.base import BaseCommand

from eatsmart.locations.durham import api


class Command(BaseCommand):
    """Import saniation data from Durham County API"""

    def handle(self, *args, **options):
        api.EstablishmentImporter().run()
        api.InspectionImporter().run()
        api.ViolationImporter().run()
