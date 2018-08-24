# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponse

from billing.models import BillingProfile, Card

import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", None)
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", None)
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
	billing_profile, created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect("cart:home")

	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url = next_

	card_qs = billing_profile.get_cards()

	context = { 
		"next_url": next_url,
		"publish_key": STRIPE_PUB_KEY,
		"card_qs": card_qs,
	}

	return render(request, 'billing/payment_method.html', context)


def payment_method_create_view(request):
	if request.method == "POST" and request.is_ajax():
		billing_profile, created = BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse({"message": "Not logged in"}, status_code=401)
	
		token = request.POST.get('token')
		if token:
			card_obj = Card.objects.add_new(billing_profile, token)
			request.session["billing_card_id"] = card_obj.stripe_id

			return JsonResponse({"message": "Done"})

	return HttpResponse("error", status_code=401)


def payment_method_reuse_view(request):
	if request.user.is_authenticated():
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None

		if request.method == "POST":
			billing_card_id = request.POST.get("billing_card_id", None)

			if billing_card_id:
				billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
				qs = Card.objects.filter(
					billing_profile=billing_profile, stripe_id=billing_card_id)
				if qs.exists():
					request.session["billing_card_id"] = billing_card_id
					if is_safe_url(redirect_path, request.get_host()):
						return redirect(redirect_path)
					else:
						return redirect("cart:checkout_review")

	return redirect("cart:checkout_login")




