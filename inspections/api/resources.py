from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.contrib.gis.resources import ModelResource as GisModelResource

from inspections.models import Establishment
from inspections.api.serializers import GeoJSONSerializer


class EstablishmentResource(GisModelResource):

    class Meta:
        queryset = Establishment.objects.all()
        allowed_methods = ['get']
        serializer = GeoJSONSerializer()
        limit = 40
        filtering = {
            'est_type': ALL,
        }
        ordering = ['update_date']
