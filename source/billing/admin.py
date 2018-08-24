# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import BillingProfile, Card, Charge

admin.site.register(BillingProfile)
admin.site.register(Card)
admin.site.register(Charge)
