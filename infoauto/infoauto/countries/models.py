# -*- coding: utf-8 -*-


from django.db import models


########################################################################


class Country(models.Model):
	
	iso = models.CharField(max_length=2, null=False, blank=False)
	name = models.CharField(max_length=255, null=False, blank=False)
	status = models.BooleanField(default=1)

	class Meta:
		ordering = ['name']


class Province(models.Model):
	
	country = models.ForeignKey("Country", null=False, blank=False, on_delete=models.PROTECT, related_name="provinces")
	name = models.CharField(max_length=255, null=False, blank=False)
	status = models.BooleanField(default=1)

	class Meta:
		ordering = ['name']


class Locality(models.Model):
	
	province = models.ForeignKey("Province", null=False, blank=False, on_delete=models.PROTECT, related_name="localities")
	name = models.CharField(max_length=255, null=False, blank=False)
	status = models.BooleanField(default=1)

	class Meta:
		ordering = ['name']


class PostalCode(models.Model):

	postal_code_number = models.PositiveIntegerField()
	locality = models.ForeignKey(
		"Locality", null=False, blank=False, on_delete=models.PROTECT, related_name="postal_codes"
	)