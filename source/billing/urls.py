from django.conf.urls import url
from .views import payment_method_view, payment_method_reuse_view, payment_method_create_view

urlpatterns = [
	url(r'^payment-method/$', payment_method_view, name="payment_method"),
	url(r'^payment_method/reuse/$', payment_method_reuse_view, name="payment_method_reuse"),
	url(r'^payment-method/create/$', payment_method_create_view, name="payment-method-create-endpoint"),
]