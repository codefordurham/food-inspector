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

@app.task
def import_durham_data_incr():
    """Import Durham data"""
    logger.info("Starting Durham Incremental Import")
    api.EstablishmentImporter().run(limit_set=True)
    lastInsp = api.InspectionImporter().get_last_inspection()
    api.InspectionImporter().run(lastInsp)
    api.ViolationImporter().run(lastInsp)
    logger.info("Finished Durham Incremental Import")
