import time
import pprint
import logging

logger = logging.getLogger(__name__)


class Importer(object):
    "Base importer logic"

    # Model class (Establishment, Inspection, Violation)
    Model = None
    # A custom ModelForm to use for validation
    Form = None

    def run(self):
        "Called to start import process"
        raise NotImplementedError("Must implement in child class")

    def get_instance(self, data, **kwargs):
        "Return model object if it exists in database"
        raise NotImplementedError("Must implement in child class")

    def map_fields(self, api, **kwargs):
        "Map field names from data source to our database schema"
        raise NotImplementedError("Must implement in child class")

    def fetch(self, data, **kwargs):
        "Primay import workflow with error handling"
        objects = []
        start_time = time.time()
        for index, api in enumerate(data):
            row = self.map_fields(api=api, **kwargs)
            try:
                instance = self.get_instance(data=row, **kwargs)
            except self.Model.DoesNotExist:
                # Instance doesn't exist, must be new
                instance = None
            form = self.Form(dict(row), instance=instance)
            if not form.is_valid():
                errors = {'model': self.Model._meta.object_name,
                          'errors': dict(form.errors.items()),
                          'cleaned_data': form.cleaned_data,
                          'api': api,
                          'row': row}
                logger.error(pprint.pformat(errors, indent=4))
                continue
            objects.append(form.save())
            if index % 20 == 0:
                elapsed_time = time.time() - start_time
                values = {'model': self.Model._meta.object_name,
                          'id': row['external_id'],
                          's': len(objects)/elapsed_time}
                msg = "{model} ID: {id} ({s:.2f} records/sec)".format(**values)
                logger.debug(msg)
                start_time = time.time()
                objects = []
