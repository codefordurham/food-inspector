# Models implement the base Local Inspector Value-Entry Specification (LIVES)
# v1.0 - http://www.yelp.com/healthscores

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy


class Establishment(models.Model):
    """Business or restaurant property"""
    STATUS_CHOICES = (('deleted', ugettext_lazy('Deleted')), ('active', ugettext_lazy('Active')))
    TYPE_CHOICES = (
        (0, ugettext_lazy('Unknown')),
        (1, ugettext_lazy('Restaurant')),
        (2, ugettext_lazy('Food Stand')),
        (3, ugettext_lazy('Mobile Food')),
        (4, ugettext_lazy('Push Cart')),
        (5, ugettext_lazy('Private School\'s Cafeteria')),
        (6, ugettext_lazy('Educational Food Service')),
        (9, ugettext_lazy('Elderly Nutrition')),
        (11, ugettext_lazy('Public School\'s Cafeteria')),
        (12, ugettext_lazy('Elderly Nutrition')),
        (14, ugettext_lazy('Limited Food')),
        (15, ugettext_lazy('Commissary (Pushcarts/Mobile Food),')),
        (16, ugettext_lazy('Institutional Food Service')),
        (20, ugettext_lazy('Lodging')),
        (21, ugettext_lazy('Bed & Breakfast Home')),
        (22, ugettext_lazy('Summer Camp')),
        (23, ugettext_lazy('Bed & Breakfast Inn')),
        (25, ugettext_lazy('Primitive Experience Camp')),
        (26, ugettext_lazy('Resident Camp')),
        (30, ugettext_lazy('Meat Market')),
        (40, ugettext_lazy('Rest/Nursing Home')),
        (41, ugettext_lazy('Hospital')),
        (42, ugettext_lazy('Child Care')),
        (43, ugettext_lazy('Residential Care')),
        (44, ugettext_lazy('School Building')),
        (45, ugettext_lazy('Local Confinement')),
        (46, ugettext_lazy('Private Boarding School/College')),
        (47, ugettext_lazy('Orphanage, Children\'s Home')),
        (48, ugettext_lazy('Adult Day Care')),
        (49, ugettext_lazy('Adult Day Service')),
        (50, ugettext_lazy('Seasonal Swimming Pool')),
        (51, ugettext_lazy('Seasonal Wading Pool')),
        (52, ugettext_lazy('Seasonal Spa')),
        (53, ugettext_lazy('Year-Round Swimming Pool')),
        (54, ugettext_lazy('Year-Round Wading Pool')),
        (55, ugettext_lazy('Year-Round Spa')),
        (61, ugettext_lazy('Tattoo Artist')),
        (72, ugettext_lazy('Summer Feeding Program')),
        (73, ugettext_lazy('Temporary Food Establishment')),
    )
    external_id = models.CharField(ugettext_lazy("External ID"), max_length=128)
    state_id = models.BigIntegerField(ugettext_lazy("State ID"))
    property_id = models.CharField(ugettext_lazy("Property ID"), max_length=128, blank=True)
    name = models.CharField(ugettext_lazy("Name"), max_length=255)
    pretty_name = models.CharField(ugettext_lazy("Pretty Name"), max_length=255, blank=True)
    type = models.PositiveIntegerField(ugettext_lazy("Type"), default=0, choices=TYPE_CHOICES)
    address = models.CharField(ugettext_lazy("Address"), max_length=255)
    city = models.CharField(ugettext_lazy("City"), max_length=64)
    county = models.CharField(ugettext_lazy("County"), max_length=64, db_index=True)
    state = models.CharField(ugettext_lazy("State"), max_length=64)
    postal_code = models.CharField(ugettext_lazy("Postal Code"), max_length=16)
    phone_number = models.CharField(ugettext_lazy("Phone Number"), max_length=64, blank=True)
    opening_date = models.DateTimeField(ugettext_lazy("Opening Date"))
    update_date = models.DateTimeField(ugettext_lazy("Update Date"), null=True, blank=True, db_index=True)
    status = models.CharField(ugettext_lazy("Status"), choices=STATUS_CHOICES, max_length=32,
                              default='active')
    location = models.PointField(ugettext_lazy("location"), null=True, blank=True)

    objects = models.GeoManager()

    class Meta(object):
        unique_together = ('external_id', 'county')

    def __str__(self):
        if (self.pretty_name):
            return self.pretty_name
        return self.name

class Inspector(models.Model):
    """Information about inspectors"""

    external_id = models.CharField(ugettext_lazy("External ID"), max_length=5)
    name = models.CharField(ugettext_lazy("Name"), max_length=128)
    phone_number = models.CharField(ugettext_lazy("Phone Number"), max_length=64, blank=True)
    e_mail = models.CharField(ugettext_lazy("E-mail address"), max_length=128, blank=True)
    county = models.CharField(ugettext_lazy("County"), max_length=64, db_index=True)
    
    class Meta(object):
        unique_together = ('external_id', 'county')

    def __str__(self):
        return self.name

class Inspection(models.Model):
    """Information about inspectors' visits to establishments"""

    TYPE_CHOICES = (
        (0, ugettext_lazy('Unknown')),
        (1, ugettext_lazy('Routine Inspection')),
        (2, ugettext_lazy('Re-inspection')),
        (5, ugettext_lazy('Permit')),
        (6, ugettext_lazy('Visit')),
        (8, ugettext_lazy('Name Change')),
        (9, ugettext_lazy('Verification')),
        (10, ugettext_lazy('Other')),
        (12, ugettext_lazy('Status Change')),
        (13, ugettext_lazy('Pre-opening Visit')),
        (31, ugettext_lazy('Critical Violation Visit')),
        (32, ugettext_lazy('Critical Violation Followup')),
    )

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=ugettext_lazy("Establishment"),
                                      related_name='inspections')
    external_id = models.CharField(ugettext_lazy("External ID"), max_length=128)
    date = models.DateTimeField(ugettext_lazy("Date"), db_index=True)
    score = models.FloatField(ugettext_lazy("Score"), null=True, blank=True)
    description = models.TextField(ugettext_lazy("Description"), blank=True)
    inspector = models.ForeignKey(Inspector,
                                     verbose_name=ugettext_lazy("Inspector"),
                                     related_name='inspections', blank=True)
    type = models.PositiveIntegerField(ugettext_lazy("Type"), default=0,
                                       choices=TYPE_CHOICES)
    update_date = models.DateTimeField(ugettext_lazy("Update Date"), null=True, blank=True,
                                       db_index=True)

    def __str__(self):
        return "Inspection #{}".format(self.pk)


class Violation(models.Model):
    """Information about specific inspection violations"""

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=ugettext_lazy("Establishment"),
                                      related_name='violations')
    inspection = models.ForeignKey(Inspection, related_name='violations',
                                   verbose_name=ugettext_lazy("Inspection"), null=True,
                                   blank=True)
    external_id = models.CharField(ugettext_lazy("External ID"), max_length=128)
    date = models.DateTimeField(ugettext_lazy("Date"), db_index=True)
    code = models.CharField(ugettext_lazy("Code"), max_length=32)
    description = models.TextField(ugettext_lazy("Description"), blank=True)
    update_date = models.DateTimeField(ugettext_lazy("Update Date"), null=True, blank=True,
                                       db_index=True)
