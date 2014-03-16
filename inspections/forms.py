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
                ]


logger = logging.getLogger(__name__)


class DateTimeFieldNull0(forms.DateTimeField):

    def to_python(self, value):
        if value in ("0", "NULL"):
            return None
        return super(DateTimeFieldNull0, self).to_python(value)


class ForceIntegerField(forms.IntegerField):
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

    bond_type_id = ForceIntegerField()
    caterer_id = ForceIntegerField()
    certified_manager_id = ForceIntegerField()
    contact_type_id = ForceIntegerField()
    county = ForceIntegerField()
    disinfectant_id = ForceIntegerField()
    district_id = ForceIntegerField()
    drivethru_id = ForceIntegerField()
    est_group_id = ForceIntegerField()
    est_type = ForceIntegerField()
    food_stamps_id = ForceIntegerField()
    handicap_access_id = ForceIntegerField()
    home_county_id = ForceIntegerField()
    inspection_type_id = ForceIntegerField()
    language_id = ForceIntegerField()
    license_type_id = ForceIntegerField()
    licensed_plumber_id = ForceIntegerField()
    menu_type_id = ForceIntegerField()
    owner_type_id = ForceIntegerField()
    permit_ehs_id = ForceIntegerField()
    pool_filter_type_id = ForceIntegerField()
    prev_state_id = ForceIntegerField()
    print_permit_id = ForceIntegerField()
    property_id = ForceIntegerField()
    renewal_status_id = ForceIntegerField()
    service_type1_id = ForceIntegerField()
    service_type2_id = ForceIntegerField()
    state_id = ForceIntegerField()
    state_owned_id = ForceIntegerField()
    update_user_id = ForceIntegerField()
    wic_id = ForceIntegerField()
    est_type = ForceIntegerField()
    territory = ForceIntegerField()
    county = ForceIntegerField()
    closing_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    construction_expiration_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    inactivate_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    last_plan_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    next_inspection_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
    opening_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
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
    update_date = DateTimeFieldNull0(input_formats=DATE_FORMATS, required=False)
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

    class Meta:
        model = Violation
