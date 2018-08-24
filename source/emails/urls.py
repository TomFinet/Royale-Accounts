from django.conf.urls import url
from .views import (
	order_confirmation_email_view,
)

urlpatterns = [
	url(r'^order-confirmation/$', order_confirmation_email_view, name="order_confirmation"),
]