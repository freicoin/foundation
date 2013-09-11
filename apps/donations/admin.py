from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(PaymentAddress)
admin.site.register(AvailableAddress)
