# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Account, AccountImage


class AccountAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']

	class Meta:
		model = Account

admin.site.register(Account, AccountAdmin)

"""class DeckCardAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'friendly_name']

	class Meta:
		model = DeckCard

admin.site.register(DeckCard, DeckCardAdmin)"""

class AccountImageAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'account']

	class Meta:
		model = AccountImage

admin.site.register(AccountImage, AccountImageAdmin)