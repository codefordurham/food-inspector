from logging import getLogger

from eatsmart.celery import app
from eatsmart.locations.durham import api
from eatsmart.locations.durham.utils import check_image
from inspections.models import Establishment

logger = getLogger(__file__)


@app.task
def import_durham_data():
    """Import Durham data"""
    logger.info("Starting Durham Import")
    api.EstablishmentImporter().run()
    api.InspectionImporter().run()
    api.ViolationImporter().run()
    logger.info("Finished Durham Import")


@app.task
def update_image_urls():
    """Iterates over all the Establishments and checks if it has a image and the
    image exists. If the image_url does not exists, use the property id to
    construct an image_url and check if the image exists."""
    for est in Establishment.objects.filter(county='Durham'):
        if est.image_url:
            image_exists = check_image(est.image_url)
            if not image_exists:
                est.image_url = ''
                est.save()
        else:
            if est.property_id:
                est.image_url = 'http://www.ustaxdata.com/nc/durham/' \
                                'photos_renamed/{0}.jpg'.format(est.property_id)
                image_exists = check_image(est.image_url)
                if image_exists:
                    est.save()
