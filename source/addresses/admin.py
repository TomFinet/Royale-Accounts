# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Address

class AddressAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'address']

	class Meta:
		model = Address

admin.site.register(Address)