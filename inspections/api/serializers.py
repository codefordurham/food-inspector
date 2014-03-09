from django.core.serializers import json as djangojson
from tastypie.serializers import Serializer


class GeoJSONSerializer(Serializer):
    """Output valid GeoJSON for Mapbox"""

    formats = ['geojson']
    content_types = {
        'geojson': 'application/json',
    }

    def to_geojson(self, data, options=None):
        """
        Given some Python data, produces GeoJSON output.
        """

        def _build_feature(obj):
            f = {
                "type": "Feature",
                "properties": {}
            }
            for key, value in obj.items():
                if key == 'location':
                    f['geometry'] = value
                if key in ['id', 'geometry']:
                    f[key] = value
                elif key == 'resource_uri':
                    pass
                else:
                    f['properties'][key] = value
            return f

        def _build_feature_collection(objs, meta):
            fc = {
                "type": "FeatureCollection",
                "features": []
            }
            if (meta):
                fc["meta"] = meta
            for obj in objs:
                fc['features'].append(_build_feature(obj))
            return fc
        options = options or {}
        data = self.to_simple(data, options)
        meta = data.get('meta')
        if 'objects' in data:
            data = _build_feature_collection(data['objects'], meta)
        else:
            data = _build_feature(data)
        return djangojson.json.dumps(data, cls=djangojson.DjangoJSONEncoder,
                                     sort_keys=True, ensure_ascii=False)
