from django.contrib import admin
from inspections.models import Establishment, Inspection, Violation
from leaflet.admin import LeafletGeoAdmin


class EstablishmentAdmin(LeafletGeoAdmin):
    search_fields = ('name', 'address')
    list_display = ('id', 'name', 'type',
                    'county', 'state_id', 'point', 'update_date')
    list_filter = ('county', 'postal_code')
    ordering = ('-update_date',)

    def point(self, obj):
        if obj.location:
            return "{}, {}".format(obj.location[0], obj.location[1])
        return None


class InspectionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'establishment__external_id', 'external_id',
                     'establishment__name')
    list_display = ('id', 'external_id', 'establishment', 'type',
                    'date', 'update_date')
    list_filter = ('update_date', 'type')
    ordering = ('-date',)
    raw_id_fields = ('establishment',)
    date_hierarchy = 'date'


class ViolationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'external_id', 'code', 'description',
                     'establishment__name')
    list_display = ('id', 'external_id', 'establishment', 'code',
                    'date', 'comments')
    list_filter = ('code',)
    raw_id_fields = ('establishment', 'inspection')
    ordering = ('-date',)
    date_hierarchy = 'date'

    def comments(self, obj):
        if obj.description:
            return "{}...".format(obj.description[:50])
        return ''


admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Violation, ViolationAdmin)
