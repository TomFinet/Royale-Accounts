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
		from_email = Email("royaleaccounts@gmail.com")
		to_email = Email("tom.finet@learning.ecolint.ch")
		subject = "Royale Accounts Order Confirmation"
		content = Content("text/plain", "and easy to do anywhere, even with Python")
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)

		return redirect("cart:success")

	return redirect("cart:home")