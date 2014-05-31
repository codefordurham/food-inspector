import logging

from django.contrib.gis import forms
from django.contrib.gis.geos import Point

from inspections.models import Establishment, Inspection, Violation


DATE_FORMATS = ['%Y%m%d']
INSPECTION_TYPE_MAP = {
    'initial': 5,  # Permit
    'routine': 1,  # Routine Inspection
    'followup': 9,  # Verification
    'complaint': 31,  # Critical Violation Followup
}
LIVES_INSPECTION_TYPES = [(x, x) for x in INSPECTION_TYPE_MAP.keys()]

logger = logging.getLogger(__name__)


class BusinessForm(forms.ModelForm):
    "Validate and clean Wake's bussiness data"

    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)

    class Meta:
        model = Establishment
        exclude = ('location',)

    def clean_city(self):
        city = self.cleaned_data['city']
        return city.title()

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
    "Validate and clean Wake's inspection data"

    establishment = forms.CharField()
    score = forms.FloatField(required=False)
    date = forms.DateTimeField(input_formats=DATE_FORMATS)
    type = forms.ChoiceField(choices=LIVES_INSPECTION_TYPES)

    class Meta:
        model = Inspection

    def clean_type(self):
        type_ = self.cleaned_data['type']
        return INSPECTION_TYPE_MAP[type_]

    def clean_establishment(self):
        query = {'county': 'Wake',
                 'external_id': self.cleaned_data['establishment']}
        try:
            return Establishment.objects.get(**query)
        except Establishment.DoesNotExist:
            raise forms.ValidationError("Establishment doesn't exist")


class ViolationForm(forms.ModelForm):
    "Validate and clean Wake's violation data"

    establishment = forms.CharField()
    inspection = forms.CharField(required=False)
    date = forms.DateTimeField(input_formats=DATE_FORMATS)

    class Meta:
        model = Violation

    def clean(self):
        cleaned_data = self.cleaned_data
        query = {'county': 'Wake',
                 'external_id': cleaned_data['establishment']}
        try:
            establishment = Establishment.objects.get(**query)
        except Establishment.DoesNotExist:
            raise forms.ValidationError("Establishment doesn't exist")
        query = {'date': cleaned_data['date'],
                 'establishment': establishment}
        try:
            inspection = Inspection.objects.get(**query)
        except Inspection.DoesNotExist:
            raise forms.ValidationError("Inspection doesn't exist")
        except Inspection.MultipleObjectsReturned:
            raise forms.ValidationError("Multiple inspections found: {}".format(str(query)))
        cleaned_data['inspection'] = inspection
        cleaned_data['establishment'] = establishment
        return cleaned_data
