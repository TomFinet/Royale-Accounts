from django.conf.urls import url
from .views import (
	JobsListView
)

urlpatterns = [
	url(r'^$', JobsListView.as_view(), name="all"),
]
