# Models implement the base Local Inspector Value-Entry Specification (LIVES)
# v1.0 - http://www.yelp.com/healthscores

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _


class Establishment(models.Model):
    """Business or restaurant property"""
    STATUS_CHOICES = (('deleted', _('Deleted')), ('active', _('Active')))
    TYPE_CHOICES = (
        (0, _('Unknown')),
        (1, _('Restaurant')),
        (2, _('Food Stand')),
        (3, _('Mobile Food')),
        (4, _('Push Cart')),
        (5, _('Private School\'s Cafeteria')),
        (6, _('Educational Food Service')),
        (9, _('Elderly Nutrition')),
        (11, _('Public School\'s Cafeteria')),
        (12, _('Elderly Nutrition')),
        (14, _('Limited Food')),
        (15, _('Commissary (Pushcarts/Mobile Food),')),
        (16, _('Institutional Food Service')),
        (20, _('Lodging')),
        (21, _('Bed & Breakfast Home')),
        (22, _('Summer Camp')),
        (23, _('Bed & Breakfast Inn')),
        (25, _('Primitive Experience Camp')),
        (26, _('Resident Camp')),
        (30, _('Meat Market')),
        (40, _('Rest/Nursing Home')),
        (41, _('Hospital')),
        (42, _('Child Care')),
        (43, _('Residential Care')),
        (44, _('School Building')),
        (45, _('Local Confinement')),
        (46, _('Private Boarding School/College')),
        (47, _('Orphanage, Children\'s Home')),
        (48, _('Adult Day Care')),
        (49, _('Adult Day Service')),
        (50, _('Seasonal Swimming Pool')),
        (51, _('Seasonal Wading Pool')),
        (52, _('Seasonal Spa')),
        (53, _('Year-Round Swimming Pool')),
        (54, _('Year-Round Wading Pool')),
        (55, _('Year-Round Spa')),
        (61, _('Tattoo Artist')),
        (72, _('Summer Feeding Program')),
        (73, _('Temporary Food Establishment')),
    )
    external_id = models.CharField(_("External ID"), max_length=128)
    state_id = models.BigIntegerField(_("State ID"))
    property_id = models.CharField(_("Property ID"), max_length=128, blank=True)
    name = models.CharField(_("Name"), max_length=255)
    type = models.PositiveIntegerField(_("Type"), default=0, choices=TYPE_CHOICES)
    address = models.CharField(_("Address"), max_length=255)
    city = models.CharField(_("City"), max_length=64)
    county = models.CharField(_("County"), max_length=64, db_index=True)
    state = models.CharField(_("State"), max_length=64)
    postal_code = models.CharField(_("Postal Code"), max_length=16)
    phone_number = models.CharField(_("Phone Number"), max_length=64, blank=True)
    opening_date = models.DateTimeField(_("Opening Date"))
    update_date = models.DateTimeField(_("Update Date"), null=True, blank=True, db_index=True)
    status = models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=32,
                              default='active')
    location = models.PointField(_("location"), null=True, blank=True)

    objects = models.GeoManager()

    class Meta(object):
        unique_together = ('external_id', 'county')

    def __str__(self):
        return self.name


class Inspection(models.Model):
    """Information about inspectors' visits to establishments"""

    TYPE_CHOICES = (
        (0, _('Unknown')),
        (1, _('Routine Inspection')),
        (2, _('Re-inspection')),
        (5, _('Permit')),
        (6, _('Visit')),
        (8, _('Name Change')),
        (9, _('Verification')),
        (10, _('Other')),
        (12, _('Status Change')),
        (13, _('Pre-opening Visit')),
        (31, _('Critical Violation Visit')),
        (32, _('Critical Violation Followup')),
    )

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=_("Establishment"),
                                      related_name='inspections')
    external_id = models.CharField(_("External ID"), max_length=128)
    date = models.DateTimeField(_("Date"), db_index=True)
    score = models.FloatField(_("Score"), null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    type = models.PositiveIntegerField(_("Type"), default=0,
                                       choices=TYPE_CHOICES)
    update_date = models.DateTimeField(_("Update Date"), null=True, blank=True,
                                       db_index=True)

    def __str__(self):
        return "Inspection #{}".format(self.pk)


class Violation(models.Model):
    """Information about specific inspection violations"""

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=_("Establishment"),
                                      related_name='violations')
    inspection = models.ForeignKey(Inspection, related_name='violations',
                                   verbose_name=_("Inspection"), null=True,
                                   blank=True)
    external_id = models.CharField(_("External ID"), max_length=128)
    date = models.DateTimeField(_("Date"), db_index=True)
    code = models.CharField(_("Code"), max_length=32)
    description = models.TextField(_("Description"), blank=True)
    update_date = models.DateTimeField(_("Update Date"), null=True, blank=True,
                                       db_index=True)
