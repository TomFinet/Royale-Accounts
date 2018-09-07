# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Email

class EmailAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'subject']

	class Meta:
		model = Email

admin.site.register(Email, EmailAdmin)
