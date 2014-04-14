import logging

from django.contrib.gis import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

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


class DateTimeFieldNull0(forms.DateTimeField):

    def to_python(self, value):
        if value in ("0", "NULL"):
            return None
        return super(DateTimeFieldNull0, self).to_python(value)


class ForceIntegerField(forms.IntegerField):
    """
    The DCO API returns decimals for fields that are really integers. Until
    Mikey fixes it, this form field forces input (floating point numbers)
    to integers.
    """

    empty_values = ['NO']

    def to_python(self, value):
        value = super(forms.IntegerField, self).to_python(value)
        if value is None or value in self.empty_values:
            return None
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value


class CleanModelChoiceField(forms.ModelChoiceField):

    def to_python(self, value):
        value = int(value)
        return super(CleanModelChoiceField, self).to_python(value)


class EstablishmentForm(forms.ModelForm):

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

    county = ForceIntegerField()
    ehs_id = ForceIntegerField()
    group_code_id = ForceIntegerField()
    est_group_id = ForceIntegerField()
    permit_status_id = ForceIntegerField()
    state_id = ForceIntegerField()
    violations_id = ForceIntegerField()
    epi_type_id = ForceIntegerField()
    territory = ForceIntegerField()
    update_user_id = ForceIntegerField()
    insp_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    setup_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    update_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    void_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    verification_required_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # these fields are missing from the current DCO API
        self.fields['action_code_id'].required = False
        self.fields['classification_id'].required = False
        self.fields['epi_type_id'].required = False
        self.fields['est_group_id'].required = False
        self.fields['est_id'].required = False
        self.fields['group_code_id'].required = False
        self.fields['inspection_reason_id'].required = False
        self.fields['oss_id'].required = False
        self.fields['permit_type_id'].required = False
        self.fields['territory'].required = False
        self.fields['update_user_id'].required = False
        self.fields['est_id'] = CleanModelChoiceField(queryset=Establishment.objects.all())

    class Meta:
        model = Inspection


class ViolationForm(forms.ModelForm):

    item = ForceIntegerField()

    class Meta:
        model = Violation
