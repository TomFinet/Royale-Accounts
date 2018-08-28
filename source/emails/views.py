# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import *


def order_confirmation_email_view(request):

	# get session variables
	to_email = request.session.get("to_email", None)
	order_id = request.session.get("order_id", None)
	accounts = request.session.get("accounts", None)

	if to_email and order_id and accounts:

		sg = sendgrid.SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))

		personalization = Personalization()
		personalization.add_to(Email(to_email))
		personalization.add_substitution(Substitution("-order_id-", order_id))
		personalization.add_substitution(Substitution("-city-", "Denver"))

		mail = Mail()
		mail.from_email = Email("royaleaccounts@gmail.com")
		mail.subject = "Royale Accounts Order Confirmation"
		mail.add_personalization(personalization)
		mail.template_id = "d-5327c993cb174d08b0aaa7e23d81f3d3"
		
		sg.client.mail.send.post(request_body=mail.get())
		
		print(response.status_code)
		print(response.body)
		print(response.headers)

		# handle errors

		return redirect("cart:success")

	return redirect("cart:home")

