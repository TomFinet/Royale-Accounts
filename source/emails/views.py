# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth import get_user_model

from users.models import AccessToken

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


User = get_user_model()
def order_confirmation_email_view(request):

	# get session variables
	to_email = request.session.get("to_email", None)
	order_id = request.session.get("order_id", None)
	accounts = request.session.get("accounts", None)

	if to_email and order_id and accounts:

		user = User.objects.filter(email=to_email)
		token, created = AccessToken.objects.new_or_get(user)

		reset_link = getattr(settings, 'WEBSITE_URL') + "user/password-reset/" + token.token

		mail = Mail()
		mail.from_email = Email('royaleaccounts@gmail.com')
		mail.subject = "Royale Accounts Order Confirmation"
		mail.template_id = 'd-5327c993cb174d08b0aaa7e23d81f3d3'
		p = Personalization()
		p.add_to(Email(to_email))
		p.dynamic_template_data = {
			'order_id': order_id,
			'accounts': accounts,
		}
		mail.add_personalization(p)

		sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))
		response = sg.client.mail.send.post(request_body=mail.get())

		if response.status_code == 202:
			return redirect("cart:success")

		# notify user that the confirmation email failed to send.

	return redirect("cart:home")

		# handle errors

		

