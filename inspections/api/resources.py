from tastypie.resources import ALL
from tastypie.contrib.gis.resources import ModelResource as GisModelResource
from django.contrib.gis.geos import Polygon

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
            'location': ALL,
        }
        ordering = ['update_date']

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(EstablishmentResource, self).build_filters(filters)

        if "within" in filters:
            bbox = filters['within'].split(',')
            orm_filters["location__within"] = Polygon.from_bbox(bbox)

        return orm_filters
