from logging import getLogger

from eatsmart.celery import app
from eatsmart.locations.wake.management.commands.import_wake import Command


logger = getLogger(__file__)

@app.task
def import_durham_data():
    """Import Raleigh data"""
    logger.info("Starting Raleigh Import")
    cmd = Command()
    cmd.handle()
    logger.info("Finished Raleigh Import")
