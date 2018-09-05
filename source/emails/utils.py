from django.conf import settings
from django.contrib.auth import get_user_model

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))

User = get_user_model()
def send_order_confirmation_email(to_email=None, order_id=None, accounts=None):
	status_code = None
	if to_email and order_id and accounts:
		'''mail = Mail()
		mail.from_email = Email('royaleaccounts@gmail.com')
		mail.subject = "Royale Accounts Order Confirmation"
		#mail.template_id = 'd-5327c993cb174d08b0aaa7e23d81f3d3'
		p = Personalization()
		p.add_to(Email(to_email))
		p.dynamic_template_data = {
			'order_id': order_id,
			'accounts': accounts,
		}
		mail.add_personalization(p)

		response = sg.client.mail.send.post(request_body=mail.get())
		status_code = response.status_code'''

		from_email = Email("royaleaccounts@gmail.com")
		subject = "Royale Accounts Order Confirmation"
		to_email = Email("tom.finet@learning.ecolint.ch")
		content = Content("text/plain", "Confirming your order.")
		mail = Mail(from_email, subject, to_email, content)
			
		response = sg.client.mail.send.post(request_body=mail.get())
		status_code = response.status_code

	return status_code

def send_password_reset_email(user=None):
	status_code = None
	if user:
		token, created = AccessToken.objects.new_or_get(user)
		if not token.is_valid():
			token.update()

		reset_link = getattr(settings, 'WEBSITE_URL') + "user/password-reset/" + token.token

		mail = Mail()
		mail.from_email = Email('royaleaccounts@gmail.com')
		mail.subject = "Royale Accounts Password Reset"
		mail.template_id = 'd-ca2e73e4409d4c94822bc282ec3fd29b'
		p = Personalization()
		p.add_to(Email(user.email))
		p.dynamic_template_data = {
			'reset_link': reset_link,
		}
		mail.add_personalization(p)

		response = sg.client.mail.send.post(request_body=mail.get())
		status_code = response.status_code

	return status_code


def send_verification_email(user=None):
	status_code = None
	if user:
		token, created = AccessToken.objects.new_or_get(user)
		verification_link = getattr(settings, 'WEBSITE_URL') + "user/v/" + token.token

		mail = Mail()
		mail.from_email = Email('royaleaccounts@gmail.com')
		mail.subject = "Verify your account with Royale Accounts"
		mail.template_id = 'd-ca2e73e4409d4c94822bc282ec3fd29b'
		p = Personalization()
		p.add_to(Email(user.email))
		p.dynamic_template_data = {
			'verification_link': verification_link,
		}
		mail.add_personalization(p)

		response = sg.client.mail.send.post(request_body=mail.get())
		status_code = response.status_code

	return status_code
