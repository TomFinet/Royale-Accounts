from __future__ import unicode_literals
from django import forms


CURRENCY_CHOICES = (
	("USD", "USD"),
	("GBP", "GBP"),
	("EUR", "EUR"),
)

class CurrencyForm(forms.Form):
	currency = forms.ChoiceField(label="", choices=CURRENCY_CHOICES, initial="USD")
