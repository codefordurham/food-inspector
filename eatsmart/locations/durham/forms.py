import logging

from django.contrib.gis import forms
from django.contrib.gis.geos import Point

from inspections.models import Establishment, Inspection, Violation


DATE_FORMATS = ['%Y-%m-%dT%H:%M:%S',     # '2006-10-25T14:30:59'
                '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
                '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
                '%Y-%m-%d',              # '2006-10-25'
                '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
                '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
                '%m/%d/%Y',              # '10/25/2006'
                '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
                '%m/%d/%y %H:%M',        # '10/25/06 14:30'
                '%m/%d/%y',              # '10/25/06'
                '%d-%b-%Y',              # '25-Oct-2006'
                '%m/%d/%Y %I:%M:%S %p',  # '12/6/2013 12:00:00 AM'
                ]


logger = logging.getLogger(__name__)


class EstablishmentForm(forms.ModelForm):
    "Validate and clean Durham's establishment data"

    status = forms.CharField()
    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)
    update_date = forms.DateTimeField(input_formats=DATE_FORMATS)
    opening_date = forms.DateTimeField(input_formats=DATE_FORMATS)

    class Meta:
        model = Establishment
        exclude = ('location',)

    def clean_status(self):
        status = self.cleaned_data['status']
        if status == 'ACTIVE':
            return 'active'
        elif status == 'DELETED':
            return 'deleted'
        raise forms.ValidationError('Invalid status')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Force empty phone value to empty string 
        if phone == '0':
            phone = ''
        return phone 

    def clean(self):
        lat = self.cleaned_data.get('lat', None)
        lon = self.cleaned_data.get('lon', None)
        if lat and lon:
            self.cleaned_data['location'] = Point(lon, lat)
        return self.cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'location' in self.cleaned_data:
            instance.location = self.cleaned_data['location']
        instance.save()
        return instance


class InspectionForm(forms.ModelForm):
    "Validate and clean Durham's inspection data"

    score = forms.FloatField(required=False)
    date = forms.DateTimeField(input_formats=DATE_FORMATS)
    update_date = forms.DateTimeField(input_formats=DATE_FORMATS)

    class Meta:
        model = Inspection

    def clean_score(self):
        # Force empty score value to None so we save to DB as NULL
        score = self.cleaned_data['score']
        if not score:
            score = None
        return score

    def clean_description(self):
        # Force API sent description strings of "NULL" to empty string
        description = self.cleaned_data['description']
        if description == 'NULL':
            description = ''
        return description


class ViolationForm(forms.ModelForm):
    "Validate and clean Durham's violation data"

    date = forms.DateTimeField(input_formats=DATE_FORMATS)
    update_date = forms.DateTimeField(input_formats=DATE_FORMATS)

    class Meta:
        model = Violation

    def clean_description(self):
        # Force API sent description strings of "0" to empty string
        description = self.cleaned_data['description']
        if description == '0':
            description = ''
        return description
