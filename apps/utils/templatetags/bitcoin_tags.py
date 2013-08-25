from django import template

from django.conf import settings

register = template.Library()

def explorer_link(explorer, element, value):
    return '<a href="%(explorer)s/%(element)s/%(value)s">%(value)s</a>' % {
        'explorer': explorer,
        'element': element,
        'value': value}

@register.filter
def frc_address(value):
    return explorer_link(settings.FRC_EXPLORER, "address", value)

@register.filter
def btc_address(value):
    return explorer_link(settings.BTC_EXPLORER, "address", value)

@register.filter
def frc_tx(value):
    return explorer_link(settings.FRC_EXPLORER, "tx", value)

@register.filter
def btc_tx(value):
    return explorer_link(settings.BTC_EXPLORER, "tx", value)
