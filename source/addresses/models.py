# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from billing.models import BillingProfile

COUNTRIES = (
	("US", "United States"),
	("CA", "Canada"),
	("UK", "United Kingdom"),
	("AF", "Afghanistan"),
	("AL", "Albania"),
	("DZ", "Algeria"),
	("AS", "American Samoa"),
	("AD", "Andorra"),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
	("", ""),
)


class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile)
	billing_first_name = models.CharField(max_length=100, default="")
	billing_last_name = models.CharField(max_length=100, default="")
	billing_country = models.CharField(choices=COUNTRIES, max_length=2, default="")
	billing_address = models.CharField(max_length=120)
	billing_city = models.CharField(max_length=100, default="")

	def __str__(self):
		return self.billing_address
