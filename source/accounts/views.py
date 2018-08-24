# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from cart.models import Cart
from .models import Account, AccountImage


class AccountsListView(ListView):
	template_name = 'accounts/accounts.html'
	paginate_by = 8
	queryset = Account.objects.filter(sold=False).order_by('-usd_price')
	context_object_name = 'account_list'

	def get_context_data(self, **kwargs):
		context = super(AccountsListView, self).get_context_data(**kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj

		conversion_rate = self.request.session.get("rate", 1)
		context["conversion_rate"] = conversion_rate

		return context

class AccountsDetailView(DetailView):
	template_name = 'accounts/details.html'
	context_object_name = 'account'

	def get_context_data(self, *args, **kwargs):
		context = super(AccountsDetailView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj

		# add the images for the account to context
		context['images'] = AccountImage.objects.filter(account=context['account'])

		conversion_rate = self.request.session.get("rate", 1)
		context["conversion_rate"] = conversion_rate

		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = Account.objects.get(slug=slug)
		except Account.DoesNotExist:
			raise Http404("Account not found.")
		except Account.MultipleObjectsReturned:
			qs = Account.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Hmmm.")
		return instance







