# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

from .forms import AddressForm

from billing.models import BillingProfile
from .models import Address

def checkout_billing_address_create_view(request):
	form = AddressForm(request.POST or None)

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		instance = form.save(commit=False)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if billing_profile:
			instance.billing_profile = billing_profile
			instance.save()
			request.session["billing_address_id"] = instance.id
		else:
			print("Error")
			return redirect("cart:checkout_login")
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)

	return redirect('cart:checkout_address')

def checkout_billing_address_reuse_view(request):
	if request.user.is_authenticated():

		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None

		if request.method == "POST":
			billing_address_id = request.POST.get("billing_address_id", None)

			if billing_address_id:
				billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
				qs = Address.objects.filter(
					billing_profile=billing_profile, id=billing_address_id)
				if qs.exists():
					request.session["billing_address_id"] = billing_address_id

			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			
	return redirect('cart:checkout_login')



