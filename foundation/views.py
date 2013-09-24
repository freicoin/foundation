from django.shortcuts import render
from django.conf import settings

def ng_app(request):
    return render(request, 'ng-app.html', 
                  {'frc_explorer': settings.FRC_EXPLORER,
                   'btc_explorer': settings.BTC_EXPLORER})

