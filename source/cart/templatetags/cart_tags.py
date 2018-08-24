from django import template

register = template.Library()

@register.simple_tag
def get_price(account, conversion_rate):
    return account.price(conversion_rate)


@register.simple_tag
def get_cart_total(cart, conversion_rate):
	return cart.total_price(conversion_rate)