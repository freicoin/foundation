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
    return explorer_link('http://cryptocoinexplorer.com:4750', "address", value)

@register.filter
def btc_address(value):
    return explorer_link('http://blockexplorer.com', "address", value)

@register.filter
def frc_tx(value):
    return explorer_link('http://cryptocoinexplorer.com:4750', "tx", value)

@register.filter
def btc_tx(value):
    return explorer_link('http://blockexplorer.com', "tx", value)
