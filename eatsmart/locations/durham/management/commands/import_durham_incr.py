from django.core.management.base import BaseCommand

from eatsmart.locations.durham import api


class Command(BaseCommand):
    """Import saniation data from Durham County API"""

    def handle(self, *args, **options):
        api.EstablishmentImporter().run(limit_set=True)
        lastInsp = api.InspectionImporter().get_last_inspection()
        api.InspectionImporter().run(limit_set=True)
        api.ViolationImporter().run(lastInsp)
