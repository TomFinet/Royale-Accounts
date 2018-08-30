# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib import messages
from django.conf import settings

from .forms import LoginForm, RegisterForm, GuestForm, EmailForm, PasswordChangeForm
from .models import GuestEmail, AccessToken
from cart.models import Cart

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def guest_register_view(request):
	form = GuestForm(request.POST or None)

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		print(form.is_valid())
		email = form.cleaned_data.get('guest_email')
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		return redirect('cart:checkout_address')
	
	return redirect("cart:checkout_login")


User = get_user_model()
def login_page(request):
	login_form = LoginForm(request.POST or None)
	
	context = {'login_form': login_form}

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if login_form.is_valid():
		email = login_form.cleaned_data.get('email')
		password = login_form.cleaned_data.get('password')

		session_user_cart, created = Cart.objects.new_or_get(request)
		session_user_accounts = session_user_cart.accounts

		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			try:
				del request.session['guest_email_id']
			except:
				pass
			if is_safe_url(redirect_path, request.get_host()):
				# transfer current cart to user cart
				user_cart, cart_created = Cart.objects.new_or_get(request)
				user_cart.accounts = session_user_accounts.all()

				return redirect(redirect_path)
			return redirect("/")
		else:
			# DJANGO messages framework to say no user with entered details found
			messages.add_message(request, messages.ERROR, 'Email or password is incorrect.', fail_silently=True)

	return render(request, 'users/login.html', context)


def register_page(request):
	register_form = RegisterForm(request.POST or None)

	context = {"register_form": register_form}

	if register_form.is_valid():
		register_form.save()
		# send email verification email
		status_code = send_verification_email(user)
		messages.success(request, """Your account has been created successfully. 
			Verify your account by clicking the link in the email sent to you""", fail_silently=True)
		return redirect("users:login")

	return render(request, "users/register.html", context)


def email_form_page(request):
	email_form = EmailForm(request.POST or None)

	if email_form.is_valid():
		# get email and send email
		email = email_form.cleaned_data.get('email')
		user = User.objects.filter(email=email).first()
		if user:
			status_code = send_password_reset_email(user)
			if status_code == 202:
				return render(request, "users/password_reset.html", {"email_sent": True, "user_id": user.id})
			messages.error(request, 'Failed to send email. Please try again.', fail_silently=True)
			# handle errors
		else:
			messages.error(request, 'User with that email does not exist.', fail_silently=True)

	return render(request, "users/password_reset.html", {"email_form": email_form})

def email_resend_view(request):
	if request.method == "POST":
		user_id = request.POST.get("user_id")
		if user_id:
			user = User.objects.get(id=user_id)
			if user:
				# send email with link
				status_code = send_password_reset_email(user)
				# check for errors
				if status_code == 202:
					count += 1
					return render(request, "users/password_reset.html", {"email_sent": True, "user_id": user.id})
				messages.error(request, 'Failed to send email. Please try again', fail_silently=True)

	email_form = EmailForm(request.POST or None)
	context = {
		"email_sent": False,
		"email_form": email_form,
	}		
	return render(request, "users/password_reset.html", context)


@login_required
def change_password_view(request):
	change_password_form = PasswordChangeForm(request.POST or None)

	if request.method == "POST":
		if change_password_form.is_valid():
			user = request.user
			old_password = change_password_form.cleaned_data.get('old_password')
			if user.check_password(old_password):
				new_password = change_password_form.cleaned_data.get('new_password1')
				if new_password != old_password:
					user.set_password(new_password)
					user.save() 
					update_session_auth_hash(request, user)
					messages.success(request, "Password changed successfully.", fail_silently=True)
				else:
					messages.error(request, "New password is the same as the old password.", fail_silently=True)
			else:
				messages.error(request, "Old password is incorrect.", fail_silently=True)

	context = {
		"change_password_form": change_password_form,
	}

	return render(request, "users/change_password.html", context)



#---------- Helper Functions -----------#

def send_password_reset_email(user):
	token, created = AccessToken.objects.new_or_get(user)
	reset_link = getattr(settings, 'WEBSITE_URL') + "user/" + token.token

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

	sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))
	response = sg.client.mail.send.post(request_body=mail.get())

	print(response.status_code)
	print(response.body)
	print(response.headers)

	return response.status_code

def send_verification_email(user):
	token, created = AccessToken.objects.new_or_get(user)
	reset_link = getattr(settings, 'WEBSITE_URL') + "user/" + token.token

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

	sg = SendGridAPIClient(apikey=getattr(settings, 'SENDGRID_API_KEY'))
	response = sg.client.mail.send.post(request_body=mail.get())

	print(response.status_code)
	print(response.body)
	print(response.headers)

	return response.status_code













