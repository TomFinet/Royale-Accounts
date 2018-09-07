# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))

class Email(models.Model):
	to = models.CharField(max_length=100)
	sender = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	content = models.TextField()

	def __str__(self):
		return '{to}: {subject}'.format(to=self.to, subject=self.subject)

	def build(self):
		to_email = Email(self.to)
		from_email = Email(self.sender)
		content_email = Content("text/html", self.content)
		mail = Mail(from_email, self.subject, to_email, content_email)
		return mail.get()

	def send(self):
		if self.to and self.sender and self.subject and self.content:
			email = self.build()
			response = sg.client.mail.send.post(request_body=email)
			return response.status_code
		return 600 # incomplete information, cannot send email.