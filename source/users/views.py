# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib import messages
from django.conf import settings

from .forms import LoginForm, RegisterForm, GuestForm, EmailForm, PasswordChangeForm, PasswordChangeTokenForm
from .models import GuestEmail, AccessToken
from cart.models import Cart

from emails.utils import send_password_reset_email, send_verification_email

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def guest_register_view(request):
	form = GuestForm(request.POST or None)

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		email = form.cleaned_data.get('guest_email')
		new_guest_email = GuestEmail.objects.new_or_update(email=email)
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
		# status_code = send_verification_email(request.user)
		messages.success(request, """Your account has been created successfully.""", fail_silently=True)
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
		else:
			messages.error(request, 'User with that email does not exist.', fail_silently=True)

	return render(request, "users/password_reset.html", {"email_form": email_form})

def reset_password_view(request, token):
	user = None
	if token:
		access_token = AccessToken.objects.get_from_token(token)
		if access_token:
			if access_token.is_valid():
				user = access_token.user
				access_token.mark_used()

	if not user:
		return render(request, "users/invalid_token.html", {})
	return change_password_helper(request, user, token)
		
@login_required
def change_password_view(request):
	return change_password_helper(request, request.user)

def change_password_token_view(request, token):
	user_token = AccessToken.objects.get_from_token(token)
	if user_token.token == token:
		return change_password_helper(request, user_token.user, token)

	return redirect("users:login")


#---------- Helper Functions -----------#

def change_password_helper(req, user, token=None):
	form = None
	if token:
		form = PasswordChangeForm(req.POST or None)
	else:
		form = PasswordChangeTokenForm(req.POST or None)

	if req.method == "POST":
		if form.is_valid():
			new_password = change_password_form.cleaned_data.get('new_password1')

			if token:
				save_new_password(req, user, new_password)
			else:
				old_password = change_password_form.cleaned_data.get('old_password')
				if user.check_password(old_password):
					if new_password != old_password:
						save_new_password(req, user, new_password)
					else:
						messages.error(req, "New password is the same as the old password.", fail_silently=True)
				else:
					messages.error(req, "Old password is incorrect.", fail_silently=True)


	context = {
		"change_password_form": form,
		"token": token,
	}

	return render(req, "users/change_password.html", context)


def save_new_password(req, user, new_password):
	user.set_password(new_password)
	user.save()
	update_session_auth_hash(req, user)
	messages.success(req, "Password changed successfully.", fail_silently=True)
		


