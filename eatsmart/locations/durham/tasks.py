from logging import getLogger

from eatsmart.celery import app
from eatsmart.locations.durham import api


logger = getLogger(__file__)


@app.task
def import_durham_data():
    """Import Durham data"""
    logger.info("Starting Durham Import")
    api.EstablishmentImporter().run()
    api.InspectionImporter().run()
    api.ViolationImporter().run()
    logger.info("Finished Durham Import")
