# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib import messages

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from cart.models import Cart

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
			print('Error')

	return render(request, 'users/login.html', context)


def register_page(request):
	register_form = RegisterForm(request.POST or None)

	context = {"register_form": register_form}

	if register_form.is_valid():
		register_form.save()
		return redirect("users:login")

	return render(request, "users/register.html", context)




