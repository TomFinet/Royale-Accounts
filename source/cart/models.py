# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from accounts.models import Account

from decimal import *

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):

	def new_or_get(self, request):
		cart_obj = None
		new_obj = True
		user = request.user

		if user.is_authenticated():
			qs = self.get_queryset().filter(user=user, active=True)
			if qs.count() == 1:
				new_obj = False
				cart_obj = qs.first()
			else:
				cart_obj = self.model.objects.new(user=user)
		else:
			cart_id = request.session.get("cart_id", None)
			qs = self.get_queryset().filter(id=cart_id, active=True)
			if qs.count() == 1:
				new_obj = False
				cart_obj = qs.first()
			else:
				cart_obj = self.model.objects.new()
				request.session["cart_id"] = cart_obj.id
		return cart_obj, new_obj
		

	def new(self, user=None):
		user_obj = None
		if (user is not None) and (user.is_authenticated()):
			user_obj = user
		return self.model.objects.create(user=user_obj)

class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	accounts = models.ManyToManyField(Account, blank=True)
	total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)

	def total_price(self, conversion_rate):
		return Decimal(Decimal(self.total) * Decimal(conversion_rate)
			).quantize(Decimal('.01'), rounding=ROUND_UP)

	def inactive(self):
		self.active = False
		self.save()

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		accounts = instance.accounts.all()
		total = 0
		for account in accounts:
			total += account.usd_price
			if instance.total != total:
				instance.total = total
				instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.accounts.through)





