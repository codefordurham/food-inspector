from django.conf.urls import patterns, url

from .views import UserAddLocationView, UserLanguageView, UserRemoveLocation


urlpatterns = patterns('',  # noqa
    url(r'^language/$',
        UserLanguageView.as_view(),
        name='users-language'),
    url(r'^location/add/$',
        UserAddLocationView.as_view(),
        name='users-location-add'),
    url(r'^location/remove/$',
        UserRemoveLocation.as_view(),
        name='users-location-remove'),
)
