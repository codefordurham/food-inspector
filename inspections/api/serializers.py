from django.core.serializers import json as djangojson
from tastypie.serializers import Serializer


class GeoJSONSerializer(Serializer):
    """Output valid GeoJSON for Mapbox"""

    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'geojson']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
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

    def to_json(self, data, options=None):
        """
        Override to enable GeoJSON generation when the geojson option is passed.
        """
        options = options or {}
        if options.get('geojson'):
            return self.to_geojson(data, options)
        else:
            return super(GeoJSONSerializer, self).to_json(data, options)
