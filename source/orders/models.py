# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.urls import reverse

from addresses.models import Address
from cart.models import Cart
from billing.models import BillingProfile, Card
from royaleaccounts.utils import unique_order_id_generator

STATUS_CHOICES = (
	("Created", "Created"),
	("Paid", "Paid"),
	("Refunded", "Refunded"),
)


class OrderManagerQuerySet(models.query.QuerySet):
	def recent(self):
		return self.order_by("-updated", "-timestamp")

	def totals_data(self):
	    return self.aggregate(Sum("total"), Avg("total"))

	def cart_data(self):
	    return self.aggregate(
	                    Sum("cart__accounts__price"), 
	                    Avg("cart__accounts__price"), 
	                    Count("cart__accounts")
	                                )

	def by_status(self, status="Paid"):
	    return self.filter(status=status)

	def not_refunded(self):
	    return self.exclude(status='Refunded')

	def by_request(self, request):
	    billing_profile, created = BillingProfile.objects.new_or_get(request)
	    return self.filter(billing_profile=billing_profile)

	def not_created(self):
	    return self.exclude(status='Created')


class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
		created = False
		qs = self.get_queryset().filter(
			billing_profile=billing_profile, 
			cart=cart_obj, 
			active=True,
			status="Created").exclude(status="Paid")
		if qs.count() == 1:
			obj = qs.first()
		else:
			obj = self.model.objects.create(
				billing_profile=billing_profile,
				cart=cart_obj)
			created = True
		return obj, created


class Order(models.Model):
	order_id = models.CharField(max_length=120, blank=True)
	billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
	billing_address = models.ForeignKey(Address, null=True, blank=True)
	cart = models.ForeignKey(Cart)
	status = models.CharField(max_length=120, default="Created", choices=STATUS_CHOICES)
	total = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	currency = models.CharField(choices=getattr(settings, "CURRENCY_CHOICES"), max_length=5)
	conversion_rate = models.DecimalField(decimal_places=2, max_digits=20, default=1.00)
	payment_card_stripe_id = models.CharField(max_length=120)

	objects = OrderManager()

	class Meta:
	   ordering = ['-timestamp', '-updated']

	def get_absolute_url(self):
	    return reverse("orders:detail", kwargs={'order_id': self.order_id})

	def __str__(self):
		return self.order_id

	def update_total(self): 
		self.total = self.cart.total
		self.save()

	def is_complete(self):
		billing_profile = self.billing_profile
		billing_address = self.billing_address
		total = self.total

		if billing_profile and billing_address and total > 0:
			return True
		return False

	# Checks that the accounts ordered have not already been purchased.
	def is_valid(self):
		order_accounts = self.cart.accounts.all()
		for account in order_accounts:
			if account.sold == True:
				return False
		return True

	def mark_paid(self):
		self.status = "Paid"
		self.active = False
		self.save()
		return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)

	qs = Order.objects.filter(
		cart=instance.cart).exclude(
		billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_obj = instance
		cart_id = cart_obj.id
		qs = Order.objects.filter(cart__id=cart_id)
		if qs.exists() and qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order, sender=Order)









