from django.conf.urls import url
from .views import AccountsListView, AccountsDetailView

urlpatterns = [
	url(r'^$', AccountsListView.as_view(), name="list"),
	url(r'^(?P<slug>[\w-]+)/', AccountsDetailView.as_view(), name="detail"),
]