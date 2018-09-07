from __future__ import unicode_literals
from django import forms

from django.conf import settings

class ContactForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}))
	email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address*'}))
	subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject*'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message*'}))

class CurrencyForm(forms.Form):
	currency = forms.ChoiceField(label="", choices=getattr(settings, "CURRENCY_CHOICES"), initial="USD")
