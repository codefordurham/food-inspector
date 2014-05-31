from django.contrib import admin
from inspections.models import Establishment, Inspection, Violation
from leaflet.admin import LeafletGeoAdmin


class EstablishmentAdmin(LeafletGeoAdmin):
    search_fields = ('name', 'address')
    list_display = ('id', 'name', 'type', 'county', 'point', 'update_date')
    list_filter = ('county', 'update_date')
    ordering = ('-update_date',)

    def point(self, obj):
        if obj.location:
            return "{}, {}".format(obj.location[0], obj.location[1])
        return None


class InspectionCountyFilter(admin.SimpleListFilter):
    title = 'County'
    parameter_name = 'county'

    def lookups(self, request, model_admin):
        counties = Establishment.objects.values_list('county', flat=True)
        return [(name, name) for name in counties.distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(establishment__county=self.value())
        else:
            return queryset


class InspectionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'establishment__external_id', 'external_id',
                     'establishment__name')
    list_display = ('id', 'establishment', 'type',
                    'date', 'external_id', 'update_date')
    list_filter = (InspectionCountyFilter, 'type', 'update_date')
    ordering = ('-date',)
    raw_id_fields = ('establishment',)
    date_hierarchy = 'date'


class ViolationCountyFilter(admin.SimpleListFilter):
    title = 'County'
    parameter_name = 'county'

    def lookups(self, request, model_admin):
        counties = Establishment.objects.values_list('county', flat=True)
        return [(name, name) for name in counties.distinct()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(inspection__establishment__county=self.value())
        else:
            return queryset


class ViolationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'external_id', 'code', 'description',
                     'establishment__name')
    list_display = ('id', 'establishment', 'code',
                    'date', 'comments', 'external_id')
    list_filter = (ViolationCountyFilter, 'date')
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
