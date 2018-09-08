# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden


from billing.models import BillingProfile, Card
from .models import Order
from addresses.models import Address
from users.models import AccessToken

class OrderListView(ListView, LoginRequiredMixin):
	template_name = 'orders/order_list.html'
	paginate_by = 3
	context_object_name = 'order_list'

	def get_queryset(self):
		return Order.objects.by_request(self.request).by_status()


class OrderDetailView(DetailView):
	template_name = 'orders/order_detail.html'
	context_object_name = 'order'

	def get_context_data(self, *args, **kwargs):
		context = super(OrderDetailView, self).get_context_data(*args, **kwargs)

		order = Order.objects.filter(order_id=context['order']).first()
		
		billing_address = Address.objects.get(id=order.billing_address.id)

		context['billing_address'] = billing_address

		payment_card = Card.objects.filter(
			billing_profile=order.billing_profile,
			stripe_id=order.payment_card_stripe_id,
		).first()

		context['payment_card'] = payment_card

		return context

	def get_object(self):
		if self.request.session.get("order_id", None):
			del self.request.session['order_id']
		
		qs = Order.objects.by_request(
		            self.request
		        ).filter(
		            order_id = self.kwargs.get('order_id')
		        )

		if qs.count() == 1:
			order = qs.first()
			user = self.request.user
			if user.is_authenticated():
				if user != order.billing_profile.user:
					raise HttpResponseForbidden()
		raise Http404()





