from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from tastypie.api import Api
from inspections.api import resources


admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(resources.EstablishmentResource())
v1_api.register(resources.InspectionResource())
v1_api.register(resources.ViolationResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name="about.html"),
        name='about'),
    (r'^api/', include(v1_api.urls)),
    url(r'^users/', include('users.urls')),
    url(r'', include('inspections.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
