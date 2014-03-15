from django.conf.urls import patterns, url

from .views import UserAddLocationView, UserRemoveLocation


urlpatterns = patterns('',  # noqa
    url(r'^location/add/$',
        UserAddLocationView.as_view(),
        name='users-location-add'),
    url(r'^location/remove/$',
        UserRemoveLocation.as_view(),
        name='users-location-remove'),
)
