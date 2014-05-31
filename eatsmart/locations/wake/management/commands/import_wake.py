from django.core.management.base import BaseCommand

from eatsmart.locations.wake import api


class Command(BaseCommand):
    """Import saniation data from Durham County API"""

    def handle(self, *args, **options):
        api.WakeCounty().import_lives()
