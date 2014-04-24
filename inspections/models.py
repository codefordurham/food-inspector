# Models implement the base Local Inspector Value-Entry Specification (LIVES)
# v1.0 - http://www.yelp.com/healthscores

from django.contrib.gis.db import models


class Establishment(models.Model):
    """Business or restaurant property"""

    STATUS_CHOICES = (('deleted', 'Deleted'), ('active', 'Active'))
    TYPE_CHOICES = (
        (0, 'Unknown'),
        (1, 'Restaurant'),
        (2, 'Food Stand'),
        (3, 'Mobile Food'),
        (4, 'Push Cart'),
        (5, 'Private School\'s Cafeteria'),
        (6, 'Educational Food Service'),
        (9, 'Elderly Nutrition'),
        (11, 'Public School\'s Cafeteria'),
        (12, 'Elderly Nutrition'),
        (14, 'Limited Food'),
        (15, 'Commissary (Pushcarts/Mobile Food),'),
        (16, 'Institutional Food Service'),
        (20, 'Lodging'),
        (21, 'Bed & Breakfast Home'),
        (22, 'Summer Camp'),
        (23, 'Bed & Breakfast Inn'),
        (25, 'Primitive Experience Camp'),
        (26, 'Resident Camp'),
        (30, 'Meat Market'),
        (40, 'Rest/Nursing Home'),
        (41, 'Hospital'),
        (42, 'Child Care'),
        (43, 'Residential Care'),
        (44, 'School Building'),
        (45, 'Local Confinement'),
        (46, 'Private Boarding School/College'),
        (47, 'Orphanage, Children\'s Home'),
        (48, 'Adult Day Care'),
        (49, 'Adult Day Service'),
        (50, 'Seasonal Swimming Pool'),
        (51, 'Seasonal Wading Pool'),
        (52, 'Seasonal Spa'),
        (53, 'Year-Round Swimming Pool'),
        (54, 'Year-Round Wading Pool'),
        (55, 'Year-Round Spa'),
        (61, 'Tattoo Artist'),
        (72, 'Summer Feeding Program'),
        (73, 'Temporary Food Establishment'),
    )
    external_id = models.CharField("External ID", max_length=128)
    state_id = models.BigIntegerField("State ID")
    property_id = models.CharField("Property ID", max_length=128, blank=True)
    name = models.CharField(max_length=255)
    type = models.PositiveIntegerField(default=0, choices=TYPE_CHOICES)
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
