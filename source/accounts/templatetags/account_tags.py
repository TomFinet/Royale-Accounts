from django import template

register = template.Library()

@register.simple_tag
def get_price(account, conversion_rate):
    return account.price(conversion_rate)