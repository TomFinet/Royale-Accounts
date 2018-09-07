# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))

class Email(models.Model):
	to = models.EmailField(max_length=100)
	sender = models.EmailField(max_length=100)
	subject = models.CharField(max_length=100)
	content = models.TextField()

	def __str__(self):
		return 'to: {to} from: {sender}'.format(to=self.to, sender=self.sender)

	def send(self):
		if self.to and self.sender and self.subject and self.content:
			to_email = Email(self.to)
			from_email = Email(self.sender)
			content = Content("text/html", self.content)
			mail = Mail(from_email, self.subject, to_email, content)
			mail.personalizations[0].add_to(Email(self.to))
			response = sg.client.mail.send.post(request_body=mail.get())
			return response.status_code
		return 600 # incomplete information, cannot send email.