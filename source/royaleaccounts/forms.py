from __future__ import unicode_literals
from django import forms

from django.conf import settings

class CurrencyForm(forms.Form):
	currency = forms.ChoiceField(label="", choices=getattr(settings, "CURRENCY_CHOICES"), initial="USD")
