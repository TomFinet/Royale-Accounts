# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render

from billing.models import BillingProfile
from .models import Order

class OrderListView(LoginRequiredMixin, ListView):
	template_name = 'orders/order_list.html'

	def get_queryset(self):
		return Order.objects.by_request(self.request).not_created()

