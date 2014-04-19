# Models implement the base Local Inspector Value-Entry Specification (LIVES)
# v1.0 - http://www.yelp.com/healthscores

from django.contrib.gis.db import models


class Establishment(models.Model):
    """Business or restaurant property"""

    STATUS_CHOICES = (('deleted', 'Deleted'), ('active', 'Active'))

    external_id = models.CharField("External ID", max_length=128)
    state_id = models.BigIntegerField("State ID")
    name = models.CharField(max_length=255)
    type = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    county = models.CharField(max_length=64, db_index=True)
    state = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=64, blank=True)
    opening_date = models.DateTimeField()
    update_date = models.DateTimeField(null=True, blank=True, db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=32,
                              default='active')
    location = models.PointField(null=True, blank=True)

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
                                      related_name='inspections')
    external_id = models.CharField("External ID", max_length=128)
    date = models.DateTimeField(db_index=True)
    score = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    type = models.PositiveIntegerField(default=0, choices=TYPE_CHOICES)
    update_date = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return "Inspection #{}".format(self.pk)


class Violation(models.Model):
    """Information about specific inspection violations"""

    establishment = models.ForeignKey(Establishment,
                                      related_name='violations')
    inspection = models.ForeignKey(Inspection, related_name='violations',
                                   null=True, blank=True)
    external_id = models.CharField("External ID", max_length=128)
    date = models.DateTimeField(db_index=True)
    code = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    update_date = models.DateTimeField(null=True, blank=True, db_index=True)
