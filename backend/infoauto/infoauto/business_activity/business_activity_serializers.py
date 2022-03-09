# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from infoauto.leads.models.business_activity import Sector, BusinessActivity


class BusinessSectorSerializer(ModelSerializer):

	class Meta:
		model = Sector
		fields = ('id', 'custom_id', 'name')


class BusinessActivitySerializer(ModelSerializer):

	sector = BusinessSectorSerializer()

	class Meta:
		model = BusinessActivity
		fields = ('id', 'custom_id', 'activity', 'sector')
