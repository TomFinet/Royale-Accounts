from django.conf.urls import url
from .views import (
	BlogPostView,
)

urlpatterns = [
	url(r'^(?P<slug>[\w-]+)/$', BlogPostView.as_view(), name="post"),
]