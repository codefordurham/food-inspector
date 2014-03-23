import json

from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class UserAddLocationView(CSRFExemptMixin, View):
    def post(self, request, *args, **kwargs):
        lat = request.POST.get('lat', '')
        lon = request.POST.get('lon', '')
        # adds the lation object into the session
        request.session['location'] = {'lat': lat, 'lon': lon}
        data = json.dumps({'status': 'success'})
        return HttpResponse(data, 'application/json')


class UserRemoveLocation(CSRFExemptMixin, View):
    def post(self, request, *args, **kwargs):
        if 'location' in request.session:
            del request.session['location']
        data = json.dumps({'status': 'success'})
        return HttpResponse(data, 'application/json')
