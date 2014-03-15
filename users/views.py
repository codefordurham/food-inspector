from decimal import Decimal
import json

from django.http import HttpResponse
from django.views.generic import View


class UserAddLocationView(View):
    def post(self, request, *args, **kwargs):
        lat = request.POST.get('lat', '')
        lon = request.POST.get('lon', '')
        # adds the lation object into the session
        request.session['location'] = {'lat': lat, 'lon': lon}
        data = json.dumps({'status': 'success'})
        return HttpResponse(data, 'application/json')


class UserRemoveLocation(View):
    def post(self, request, *args, **kwargs):
        if 'location' in request.session:
            del request.session['location']
        data = json.dumps({'status': 'success'})
        return HttpResponse(data, 'application/json')
