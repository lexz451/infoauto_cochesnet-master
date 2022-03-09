# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views_rest import LocalitiesDetail, Localities, ProvincesDetail, Provinces, CountriesDetail, Countries

urlpatterns = [
    url(r'^countries/$', Countries.as_view()),  # Países - Listado (GET)
    url(r'^countries/(?P<pk>\d+)/$', CountriesDetail.as_view()),  # Países - Obtención (GET)
    url(r'^provinces/$', Provinces.as_view()),  # Provincias - Listado (GET)
    url(r'^provinces/(?P<pk>\d+)/$', ProvincesDetail.as_view()),  # Provincias - Obtención (GET)
    url(r'^localities/$', Localities.as_view()),  # Localidades - Listado (GET)
    url(r'^localities/(?P<pk>\d+)/$', LocalitiesDetail.as_view()),  # Localidades - Obtención (GET)
]

