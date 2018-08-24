# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from users.models import GuestEmail

import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", None)
stripe.api_key = STRIPE_SECRET_KEY

class BillingProfileManager(models.Manager):

	def new_or_get(self, request):
		obj = None
		created = False
		user = request.user
		guest_email_id = request.session.get('guest_email_id')

		if user.is_authenticated():
			obj, created = self.model.objects.get_or_create(
				user=user, email=user.email)
		elif guest_email_id is not None:
			guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
			obj, created = BillingProfile.objects.get_or_create(
				email=guest_email_obj.email)
		else:
			pass
		return obj, created


User = settings.AUTH_USER_MODEL
class BillingProfile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	customer_id = models.CharField(max_length=120, null=True, blank=True)

	objects = BillingProfileManager()

	def __str__(self):
		return self.email

	def charge(self, order_obj, card=None, currency="USD"):
		return Charge.objects.do(self, order_obj, card, currency)

	def get_cards(self):
		return self.card_set.all()

	def payment_card(self, stripe_id):
		return self.get_cards().filter(stripe_id=stripe_id).first()

	@property
	def has_card(self):
		instance = self
		card_qs = self.get_cards()
		return card_qs.exists()

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
                email = instance.email
            )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

def user_created_receiver(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
	def add_new(self, billing_profile, token):
		if token:
			customer = stripe.Customer.retrieve(billing_profile.customer_id)
			stripe_card_resp = customer.sources.create(source=token)
			new_card = self.model(
				billing_profile=billing_profile,
				stripe_id=stripe_card_resp.id,
				brand=stripe_card_resp.brand,
				country=stripe_card_resp.country,
				exp_month=stripe_card_resp.exp_month,
				exp_year=stripe_card_resp.exp_year,
				last4=stripe_card_resp.last4
			)
			new_card.save()
			return new_card
		return None


class Card(models.Model):
	billing_profile = models.ForeignKey(BillingProfile)
	stripe_id = models.CharField(max_length=120)
	brand = models.CharField(max_length=120, null=True, blank=True)
	country = models.CharField(max_length=120, null=True, blank=True)
	exp_month = models.IntegerField(null=True, blank=True)
	exp_year = models.IntegerField(null=True, blank=True)
	last4 = models.CharField(max_length=4, null=True, blank=True)

	objects = CardManager()

	def __str__(self):
		return "{} {}".format(self.brand, self.last4)



class ChargeManager(models.Manager):
	def do(self, billing_profile, order_obj, card=None, currency="USD"):
		card_obj = card
		if card_obj is None:
			return False, "No cards available"

		charge = stripe.Charge.create(
			amount=int(order_obj.total * 100),
			currency=currency,
			customer=billing_profile.customer_id,
			source=card_obj.stripe_id,
			metadata={"order_id": order_obj.order_id},
		)

		charge_obj = self.model(
			billing_profile=billing_profile,
			stripe_id=charge.id,
			paid=charge.paid,
			refunded=charge.refunded,
			outcome=charge.outcome,
			outcome_type=charge.outcome['type'],
			seller_message=charge.outcome['seller_message'],
			risk_level=charge.outcome['risk_level'],
		)
		charge_obj.save()
		return charge_obj.paid, charge_obj.seller_message


class Charge(models.Model):
	billing_profile = models.ForeignKey(BillingProfile)
	stripe_id = models.CharField(max_length=120)
	paid = models.BooleanField(default=False)
	refunded = models.BooleanField(default=False)
	outcome = models.TextField(null=True, blank=True)
	outcome_type = models.CharField(max_length=120, null=True, blank=True)
	seller_message = models.CharField(max_length=120, null=True, blank=True)
	risk_level = models.CharField(max_length=120, null=True, blank=True)

	objects = ChargeManager()




	


