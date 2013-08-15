from django import template

from django.conf import settings

register = template.Library()

@register.filter
def frc_address(value):
    return '<a href="%(explorer)s/address/%(address)s">%(address)s</a>' % {
        'explorer': settings.FRC_EXPLORER,
        'address': value}

@register.filter
def btc_address(value):
    return '<a href="%(explorer)s/address/%(address)s">%(address)s</a>' % {
        'explorer': settings.BTC_EXPLORER,
        'address': value}

@register.filter
def frc_tx(value):
    return '<a href="%(explorer)s/tx/%(address)s">%(address)s</a>' % {
        'explorer': settings.FRC_EXPLORER,
        'address': value}

@register.filter
def btc_tx(value):
    return '<a href="%(explorer)s/tx/%(address)s">%(address)s</a>' % {
        'explorer': settings.BTC_EXPLORER,
        'address': value}
