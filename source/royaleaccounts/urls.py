from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from .views import home_view, FaqView, TermsOfUseView, currency_convert_view

urlpatterns = [
	url(r'^$', home_view, name="home"),
    url(r'^faq/$', FaqView.as_view(), name="faq"),
    url(r'^terms-of-use/$', TermsOfUseView.as_view(), name="terms_of_use"),
    url(r'^currency/convert/$', currency_convert_view, name="currency_convert_view"),

	url(r'^address/', include('addresses.urls', namespace="addresses")),
    url(r'^user/', include('users.urls', namespace="users")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^cart/', include('cart.urls', namespace="cart")),
    url(r'^billing/', include('billing.urls', namespace="billing")),
    url(r'^orders/', include('orders.urls', namespace="orders")),
    url(r'^blog/', include('blogs.urls', namespace="blogs")),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)