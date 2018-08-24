from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('billing_country', 'billing_first_name', 'billing_last_name', 'billing_address', 'billing_city')

	def __init__(self, *args, **kwargs):
	    super(AddressForm, self).__init__(*args, **kwargs)
	    for field in self.Meta.fields:
	        self.fields[field].widget.attrs.update({
	            'class': 'form-control'
	        })