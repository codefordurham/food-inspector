from django.contrib import admin
from inspections.models import Establishment, Inspection, Violation
from leaflet.admin import LeafletGeoAdmin


class EstablishmentAdmin(LeafletGeoAdmin):
    search_fields = ('premise_name', 'owner_name')
    list_display = ('id', 'premise_name', 'est_type', 'update_date',
                    'state_id', 'point')
    list_filter = ('type_description',)
    ordering = ('-update_date',)

    def point(self, obj):
        return "{}, {}".format(obj.location[0], obj.location[1])


class InspectionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'est_id__id', 'est_id__premise_name')
    list_display = ('id', 'est_id', 'insp_date', 'classification_desc')
    list_filter = ('classification_desc',)
    ordering = ('-insp_date',)


class ViolationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'inspection_id__id')
    list_display = ('id', 'inspection_id', 'weight_sum', 'comments')
    list_filter = ('item',)
    raw_id_fields = ('inspection_id',)
    ordering = ('-inspection_id',)


admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Violation, ViolationAdmin)
