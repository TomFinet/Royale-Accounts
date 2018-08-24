from django.conf.urls import url
from .views import (
	cart_api_view,
	cart_home, 
	cart_update, 
	checkout_login,
	checkout_address,
	checkout_review,
	checkout_payment,
	checkout_complete_view,
)

urlpatterns = [
	url(r'^api/$', cart_api_view, name="api"),
	url(r'^$', cart_home, name="home"),
	url(r'^update/$', cart_update, name="update"),
	url(r'^checkout/login/$', checkout_login, name="checkout_login"),
	url(r'^checkout/billing-address/$', checkout_address, name="checkout_address"),
	url(r'^checkout/review/$', checkout_review, name="checkout_review"),
	url(r'^checkout/payment/$', checkout_payment, name="checkout_payment"),
	url(r'^checkout/success/$', checkout_complete_view, name="success"),
]