# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

from users.models import GuestEmail
from accounts.models import Account
from .models import Cart
from billing.models import BillingProfile, Card
from orders.models import Order
from addresses.models import Address
from emails.utils import send_order_confirmation_email

from addresses.forms import AddressForm
from users.forms import LoginForm, GuestForm
from royaleaccounts.forms import CurrencyForm

from decimal import *


def cart_api_view(request):
	if request.is_ajax():
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		conversion_rate = request.session.get("rate", 1)
		currency = request.session.get("currency", "USD")

		accounts = serialize_accounts(cart_obj.accounts.all(), conversion_rate)

		return JsonResponse({
			"accounts": accounts, 
			"total": Decimal(Decimal(cart_obj.total) * Decimal(conversion_rate)
				).quantize(Decimal('.01'), rounding=ROUND_UP),
			"currency": currency,
		})
	return redirect("cart:home")


def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	conversion_rate = request.session.get("rate", 1)

	context = {
		"cart": cart_obj,
		"conversion_rate": conversion_rate,
		"cart_total": cart_obj.total_price(conversion_rate)
	}

	return render(request, "cart/home.html", context)


def cart_update(request):
	account_id = request.POST.get("account_id")
	if account_id is not None:
		added = False
		try:
			account_obj = Account.objects.get(id=account_id)
		except Account.DoesNotExist:
			return redirect("cart:home")
		
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if account_obj in cart_obj.accounts.all():
			cart_obj.accounts.remove(account_obj)
		else:
			cart_obj.accounts.add(account_obj)
			added = True
		request.session["cart_items_count"] = cart_obj.accounts.count()

		if request.is_ajax():
			json_data = {
				"added": added,
				"cartItemCount": cart_obj.accounts.count()
			}
			return JsonResponse(json_data)

	return redirect("cart:home")

# ensures the user is logged in or is guest.
def checkout_login(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	if cart_created or cart_obj.accounts.count() == 0:
		return redirect("cart:home")
	
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	if not billing_profile:
		login_form = LoginForm()
		guest_form = GuestForm()

		context = {'login_form': login_form, "guest_form": guest_form}

		return render(request, 'cart/checkout_login.html', context)
	return redirect('cart:checkout_address')


# loads address form and if logged in the addresses previously used.
def checkout_address(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	if cart_created or cart_obj.accounts.count() == 0:
		return redirect("cart:home")

	address_qs = None
	billing_address_form = AddressForm()

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if billing_profile:
		if request.user.is_authenticated():
			address_qs = Address.objects.filter(billing_profile=billing_profile)

		billing_address_id = request.session.get("billing_address_id", None)
		if billing_address_id:
			order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
			order_obj.save()
			return redirect("billing:payment_method")
	else:
		return redirect('cart:checkout_login')

	context = {
		"billing_address_form": billing_address_form,
		"address_qs": address_qs,
	}

	return render(request, 'cart/checkout_address.html', context)
			

def checkout_review(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	if cart_created or cart_obj.accounts.count() == 0:
		return redirect("cart:home")

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if billing_profile:
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		billing_address = order_obj.billing_address

		if billing_address is None:
			return redirect("cart:checkout_address")

		stripe_id = request.session.get('billing_card_id', None)
		billing_card = billing_profile.payment_card(stripe_id)

		if billing_card is None:
			return redirect("billing:payment_method")

		conversion_rate = request.session.get("rate", 1)

		context = {
			"cart": cart_obj,
			"billing_address": billing_address,
			"billing_card": billing_card,
			"conversion_rate": conversion_rate,
		}

		return render(request, 'cart/checkout_review.html', context)

	return redirect("cart:home")


def checkout_payment(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	if cart_created or cart_obj.accounts.count() == 0:
		return redirect("cart:home")

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	if billing_profile:
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
	
		if request.method == "POST":
			if order_obj.is_complete():
				if order_obj.is_valid():

					stripe_id = request.session.get('billing_card_id', None)
					billing_card = billing_profile.payment_card(stripe_id)
					currency = request.session.get("currency", "USD")

					did_charge, charge_msg = billing_profile.charge(
						order_obj, billing_card, currency
					)

					if did_charge:
						order_obj.mark_paid()

						qs = order_obj.cart.accounts.all()
						conversion_rate = request.session.get("rate", 1)
						accounts = serialize_accounts(qs, conversion_rate)

						order_obj.currency = currency
						order_obj.conversion_rate = conversion_rate
						order_obj.payment_card_stripe_id = stripe_id
						order_obj.updated = timezone.now()
						order_obj.save()

						for account in qs:
							account.sold = True
							account.save()
							
						cart_obj.inactive()

						del request.session["billing_card_id"]
						if not request.user.is_authenticated():
							del request.session["cart_id"]
						del request.session["cart_items_count"]

						status_code = send_order_confirmation_email(
							billing_profile.email, 
							order_obj.order_id, 
							accounts
						)

						messages.success(request, "Order paid successfully.")

						if status_code != 202:
							messages.error(request, "Failed to send confirmation email.")
						else:
							messages.success(request, "Confirmation email sent successfully.")
						return redirect("cart:success")
						
					else:
						print(charge_msg)
						return redirect("cart:checkout_login")
				else:
					# Remove all items from cart since some items have already been purchased.
					cart_obj.accounts.clear()
					# redirect to error page
					request.session['from_payment'] = True
					return redirect("cart:error")

	return redirect("cart:checkout_login")

def checkout_error_view(request):
	if request.session.get('from_payment', False):
		del request.session['from_payment']
		return render(request, "cart/error.html", {})
	return redirect("cart:home")

def checkout_complete_view(request):
	return render(request, "cart/checkout_done.html", {})


#------ Helper Functions -------#

def serialize_accounts(accounts_qs, conversion_rate):
	accounts = []
	for a in accounts_qs:
		img_sml_url = None
		try:
			img_sml_url = a.img_sml.url
		except:
			pass

		accounts.append({
			"id": a.id,
			"url": a.get_absolute_url(),
			"title": a.title, 
			"price": float(Decimal(Decimal(a.usd_price) * Decimal(conversion_rate)
				).quantize(Decimal('.01'), rounding=ROUND_UP)),
			"img_sml_url": img_sml_url,
		})

	return accounts

