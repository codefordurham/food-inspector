import logging

from django.contrib.gis import forms
from django.contrib.gis.geos import Point

from inspections.models import Establishment


DATE_FORMATS = ['%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
                '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
                '%Y-%m-%d',              # '2006-10-25'
                '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
                '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
                '%m/%d/%Y',              # '10/25/2006'
                '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
                '%m/%d/%y %H:%M',        # '10/25/06 14:30'
                '%m/%d/%y',              # '10/25/06'
                '%d-%b-%Y']              # 25-Oct-2006


logger = logging.getLogger(__name__)


class DateTimeFieldNull0(forms.DateTimeField):

    def to_python(self, value):
        if value == "0":
            return None
        return super(DateTimeFieldNull0, self).to_python(value)


class EstablishmentForm(forms.ModelForm):

    closing_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    construction_expiration_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    inactivate_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    last_plan_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    next_inspection_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    permit_expiration_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    permit_print_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    reactivate_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    renewal_received_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    renewal_sent_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    setup_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    status_change_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    test_expiration_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    status_change_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    test_expiration_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)
    location = forms.PointField(required=False)

    class Meta:
        model = Establishment

    def clean(self):
        lat = self.cleaned_data.get('lat', None)
        lon = self.cleaned_data.get('lon', None)
        if lat and lon:
            self.cleaned_data['location'] = Point(lon, lat)
        return self.cleaned_data
