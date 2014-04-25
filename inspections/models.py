# Models implement the base Local Inspector Value-Entry Specification (LIVES)
# v1.0 - http://www.yelp.com/healthscores

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _


class Establishment(models.Model):
    """Business or restaurant property"""

    STATUS_CHOICES = (('deleted', _('Deleted')), ('active', _('Active')))

    external_id = models.CharField(_("External ID"), max_length=128)
    state_id = models.BigIntegerField(_("State ID"))
    property_id = models.CharField(_("Property ID"), max_length=128, blank=True)
    name = models.CharField(_("name"), max_length=255)
    type = models.PositiveIntegerField(_("type"), default=0)
    address = models.CharField(_("address"), max_length=255)
    city = models.CharField(_("city"), max_length=64)
    county = models.CharField(_("county"), max_length=64, db_index=True)
    state = models.CharField(_("state"), max_length=64)
    postal_code = models.CharField(_("postal code"), max_length=16)
    phone_number = models.CharField(_("phone number"), max_length=64,
                                    blank=True)
    opening_date = models.DateTimeField(_("opening date"))
    update_date = models.DateTimeField(_("update date"), null=True, blank=True,
                                       db_index=True)
    status = models.CharField(_("status"), choices=STATUS_CHOICES, max_length=32,
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
        (0, 'Unknown'),
        (1, 'Routine Inspection'),
        (2, 'Re-inspection'),
        (5, 'Permit'),
        (6, 'Visit'),
        (8, 'Name Change'),
        (9, 'Verification'),
        (10, 'Other'),
        (12, 'Status Change'),
        (13, 'Pre-opening Visit'),
        (31, 'Critical Violation Visit'),
        (32, 'Critical Violation Followup'),
    )

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=_("establishment"),
                                      related_name='inspections')
    external_id = models.CharField(_("External ID"), max_length=128)
    date = models.DateTimeField(_("date"), db_index=True)
    score = models.FloatField(_("score"), null=True, blank=True)
    description = models.TextField(_("description"), blank=True)
    type = models.PositiveIntegerField(_("type"), default=0,
                                       choices=TYPE_CHOICES)
    update_date = models.DateTimeField(_("update date"), null=True, blank=True,
                                       db_index=True)

    def __str__(self):
        return "Inspection #{}".format(self.pk)


class Violation(models.Model):
    """Information about specific inspection violations"""

    establishment = models.ForeignKey(Establishment,
                                      verbose_name=_("establishment"),
                                      related_name='violations')
    inspection = models.ForeignKey(Inspection, related_name='violations',
                                   verbose_name=_("inspection"), null=True,
                                   blank=True)
    external_id = models.CharField(_("External ID"), max_length=128)
    date = models.DateTimeField(_("date"), db_index=True)
    code = models.CharField(_("date"), max_length=32)
    description = models.TextField(_("description"), blank=True)
    update_date = models.DateTimeField(_("update date"), null=True, blank=True,
                                       db_index=True)
