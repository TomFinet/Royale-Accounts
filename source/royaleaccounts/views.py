from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.core.cache import cache

from cart.models import Cart
from accounts.models import Account

from .forms import ContactForm

from emails.utils import send_contact_us_email

import requests
from decimal import *

CURRENCY_BASE_URL = getattr(settings, "CURRENCY_BASE_URL", None)
CURRENCY_ACCESS_KEY = getattr(settings, "CURRENCY_ACCESS_KEY", None)

def home_view(request):
	# IMPROVEMENT: Don't create cart every time the page is loaded.
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	request.session["cart_items_count"] = cart_obj.accounts.count()

	# get account images
	featured_qs = Account.objects.filter(sold=False)

	return render(request, 'index.html', {"featured_qs": featured_qs})


def contact_view(request):
	form = ContactForm(request.POST or None)

	if form.is_valid() and request.method == "POST":
		name = form.cleaned_data.get('name')
		sender = form.cleaned_data.get('email')
		subject = form.cleaned_data.get('subject')
		message = form.cleaned_data.get('message')
		status_code = send_contact_us_email(sender, name, subject, message)

		if status_code != 202:
			messages.error(request, "Failed to send email. Try sending it through your email account if this problem persists.")
		else:
			messages.success(request, "Message sent successfully, expect a reply within 48 hours.")
			form = ContactForm()

	return render(request, 'contact_us.html', {"form": form})


class FaqView(TemplateView):
	template_name = 'faq.html'


class TermsOfUseView(TemplateView):
	template_name = 'terms_of_use.html'

# add cache expiry
def currency_convert_view(request):
	if request.is_ajax():
		to_ = request.POST.get('currency', "USD")
		if to_:
			conversion_rate = cache.get("usd_to_{to}".format(to=to_.lower()), None)
			if not conversion_rate:
				response = requests.get(CURRENCY_BASE_URL +
					"?api_key=" + CURRENCY_ACCESS_KEY + 
					"&from=USD" + "&to=" + to_
				)
				json_response = response.json()
				conversion_rate = json_response["amount"]
				if conversion_rate == 0:
					# error should probably return to the current page and display error message
					conversion_rate = 1
				else:
					cache.set("usd_to_{to}".format(to=to_.lower()), conversion_rate)


			accounts = Account.objects.filter(sold=False).order_by('-usd_price')
			account_prices = [
				Decimal(Decimal(a.usd_price) * Decimal(conversion_rate))
					.quantize(Decimal('.01'), rounding=ROUND_UP)
				for a in accounts
			]

			account_id = request.POST.get("account_id")
			account = accounts.filter(id=account_id).first()
			detail_price = 0
			if account:
				detail_price = account.price(Decimal(conversion_rate))

			# cart prices now
			# get the cart items and multiply prices by conversion rate
			cart_obj, new_obj = Cart.objects.new_or_get(request)
			cart_accounts = cart_obj.accounts.all()
			cart_prices = [
				Decimal(Decimal(a.usd_price) * Decimal(conversion_rate)
					).quantize(Decimal('.01'), rounding=ROUND_UP)
				for a in cart_accounts
			]
			cart_total = Decimal(Decimal(cart_obj.total) * Decimal(conversion_rate)
				).quantize(Decimal('.01'), rounding=ROUND_UP)

			request.session["currency"] = to_
			request.session["rate"] = conversion_rate

			return JsonResponse({
				"currency": to_,
				"account_prices": account_prices,
				"detail_account_price": detail_price,
				"cart_prices": cart_prices,
				"cart_total": cart_total,
			})
			
	return redirect("home")

























