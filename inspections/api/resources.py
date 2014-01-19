from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource as GisModelResource

from inspections.models import Establishment
from inspections.api.serializers import GeoJSONSerializer


class EstablishmentResource(GisModelResource):
    class Meta:
        queryset = Establishment.objects.all()
        allowed_methods = ['get']
        serializer = GeoJSONSerializer()
