from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from inspections.models import Establishment, Inspection, Violation
from leaflet.admin import LeafletGeoAdmin


class ImageFilter(SimpleListFilter):
    title = _('Image')

    parameter_name = 'image'

    def lookups(self, request, model_admin):
        return (
            ('all', _('All')),
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': (self.value() == force_text(lookup) or
                             not self.value() and force_text(lookup) == "all"),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        value = self.value()
        if not value == 'all':
            if value == 'yes':
                return queryset.exclude(image_url='')
            else:
                return queryset.filter(image_url='')
        return queryset


class EstablishmentAdmin(LeafletGeoAdmin):
    search_fields = ('name', 'address')
    list_display = ('id', 'name', 'type', 'county', 'state_id', 'image',
                    'point', 'update_date')
    list_filter = ('county', ImageFilter, 'postal_code')
    ordering = ('-update_date',)

    def point(self, obj):
        if obj.location:
            return "{}, {}".format(obj.location[0], obj.location[1])
        return None

    def image(self, obj):
        if not obj.image_url:
            return ''
        return u'<a href="{0}"><img src="/static/admin/img/icon-yes.gif" />' \
               u'</a>'.format(obj.image_url)
    image.allow_tags = True


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
