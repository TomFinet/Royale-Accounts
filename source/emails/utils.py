from django.contrib.auth import get_user_model

from users.models import AccessToken
from .models import Email


User = get_user_model()
def send_order_confirmation_email(to_email=None, order_id=None, accounts=None):
	status_code = None
	if to_email and order_id and accounts:
		from_ = "order@royale-accounts.com"
		subject = "Royale Accounts Order Confirmation"
		content = """<h4>Thank you so much for placing your order with Royale Accounts.</h4> 
		You can view your order by clicking this link: <a href='https://www.royale-accounts.com/orders/""" 
		+ order_id + """'><h4>Your Order</h4></a>
		Once again thank you so much for placing your order with us.<br>
		Happy Clashing,<br>
		The Royale Accounts Team."""
			
		email = Email.objects.create(to=to_email, sender=from_, subject=subject, content=content)
		status_code = email.send()

	return status_code

def send_password_reset_email(user=None):
	status_code = None
	if user:
		token, created = AccessToken.objects.new_or_get(user)
		if not token.is_valid():
			token.update()

		reset_link = getattr(settings, 'WEBSITE_URL') + "user/password-reset/" + token.token

		from_ = "support@royale-accounts.com"
		subject = "Royale Accounts Password Reset"
		content = """It seems you have forgotten your password. Just click the link to reset your password:
			<a href='""" + reset_link + """'><h4>Reset your Royale Accounts password</h4></a>"""
			
		email = Email.objects.create(to=user.email, sender=from_, subject=subject, content=content)
		status_code = email.send()

	return status_code


def send_verification_email(user=None):
	status_code = None
	if user:
		token, created = AccessToken.objects.new_or_get(user)
		verification_link = getattr(settings, 'WEBSITE_URL') + "user/v/" + token.token

		from_ = "support@royale-accounts.com"
		subject = "Verify your Royale Accounts account"
		content = """To verify your account just click the link:
			<a href='""" + verification_link + """'><h4>Verify your Royale Accounts account</h4></a>"""
			
		email = Email.objects.create(to=user.email, sender=from_, subject=subject, content=content)
		status_code = email.send()

	return status_code








