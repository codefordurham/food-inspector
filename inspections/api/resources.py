from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.contrib.gis.resources import ModelResource as GisModelResource
from django.contrib.gis.geos import Polygon

from inspections.models import Establishment, Inspection
from inspections.api.serializers import GeoJSONSerializer


class EstablishmentResource(GisModelResource):

    class Meta(object):
        queryset = Establishment.objects.all()
        allowed_methods = ['get']
        serializer = GeoJSONSerializer()
        limit = 40
        filtering = {
            'est_type': ALL,
            'location': ALL,
            'premise_name': ALL,
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


class InspectionResource(ModelResource):
    est_id = fields.ForeignKey(EstablishmentResource, 'est_id')

    class Meta(object):
        queryset = Inspection.objects.all()
        allowed_methods = ['get']
        limit = 20
        insp_date = ['update_date']
        filtering = {
            'est_id': ALL,
        }
