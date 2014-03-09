from django.conf.urls import patterns, url

from inspections import views

urlpatterns = patterns('',  # noqa
    url(r'^$', views.EstablishmentList.as_view(), name='establishment-list'),
    url(r'^(?P<pk>\d+)/$', views.EstablishmentDetail.as_view(),
        name='establishment-detail'),
)
