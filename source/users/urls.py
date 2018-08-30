from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import (
	login_page,
	register_page,
	guest_register_view,
	email_form_page,
	email_resend_view,
	change_password_view,
)


urlpatterns = [
	url(r'^logout/', LogoutView.as_view(), name="logout"),
	url(r'^login/', login_page, name="login"),
	url(r'^register/', register_page, name="register"),
	url(r'^register-guest/', guest_register_view, name="guest_register"),


	url(r'^password-reset-email/$', email_form_page, name="password_reset_email"),
	url(r'^password-reset/resend/$', email_resend_view, name="password_reset_resend_email"),
	url(r'^change-password/$', change_password_view, name="change_password"),
	#url(r'^password-reset/(?P<token>[0-9A-Za-z]{1,16})/(?P<user_id>[\d+]+)$',
		#.as_view(), name='activate_account'),
]