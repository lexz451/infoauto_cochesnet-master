# -*- coding: utf-8 -*-

import django_filters
from rest_framework import mixins

from . import models
from . import serializers

from rest_framework.viewsets import GenericViewSet

from .models import PostalCode


class Countries(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    search_fields = ("name",)


class ProvincesFilter(django_filters.FilterSet):
    class Meta:
        model = models.Province
        fields = ("country",)


class Provinces(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    filter_class = ProvincesFilter
    search_fields = ("name", )

    def list(self, request, *args, **kwargs):
        if "country" in request.GET:
            self.queryset = self.queryset.filter(country=request.GET.get("country"))
        return super().list(request, *args, **kwargs)


class LocalitiesFilter(django_filters.FilterSet):
    country = django_filters.ModelChoiceFilter(field_name="province__country",
                                               queryset=models.Country.objects.all())

    class Meta:
        model = models.Locality
        fields = ("country", "province")


class Localities(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Locality.objects.all().order_by('id')
    serializer_class = serializers.LocalityFullSerializer
    filter_class = LocalitiesFilter
    search_fields = ("name", )

    def list(self, request, *args, **kwargs):
        if "province" in request.GET:
            self.queryset = self.queryset.filter(province=request.GET.get("province"))

        if "postal_code" in request.GET:
            localities_pks = PostalCode.objects.filter(
                postal_code_number=request.GET.get("postal_code")
            ).values_list('locality_id', flat=True)

            self.queryset = self.queryset.filter(id__in=localities_pks)

        return super().list(request, *args, **kwargs)
