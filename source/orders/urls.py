from django.conf.urls import url
from .views import (
    OrderListView
)

urlpatterns = [
    url(r'^list/$', OrderListView.as_view(), name="list"),
]