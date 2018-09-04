# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render
from django.http import Http404

from billing.models import BillingProfile
from .models import Order

class OrderListView(ListView):
	template_name = 'orders/order_list.html'
	paginate_by = 3
	context_object_name = 'order_list'

	def get_queryset(self):
		return Order.objects.by_request(self.request).by_status()


class OrderDetailView(DetailView):
	template_name = 'orders/order_detail.html'
	context_object_name = 'order'

	def get_object(self):
		qs = Order.objects.by_request(
		            self.request
		        ).filter(
		            order_id = self.kwargs.get('order_id')
		        )
		if qs.count() == 1:
		    return qs.first()
		raise Http404