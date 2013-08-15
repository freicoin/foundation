from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.db.models import Q

from datetime import datetime, timedelta

from apps.faucet.models import *
from apps.faucet import forms
from foundation import utils

def recent_sends(request):
    sends = FaucetSend.objects.order_by('-timestamp')[:20]
    return render(request, 'recent_sends.html', {'send_list': sends})

def faucet(request):
    if request.method == 'POST':
        form = forms.FaucetForm(request.POST)

        if form.is_valid():

            send = FaucetSend()
            send.frc_address = form.cleaned_data['frc_address']
            send.ip_address = utils.get_client_ip(request)

            enddate = datetime.now() 
            startdate = enddate - timedelta(days=1)

            conflict_sends = FaucetSend.objects.filter(
                timestamp__range=[startdate, enddate]).filter(
                Q(frc_address=send.frc_address) 
                | Q(ip_address=send.ip_address))

            if ( conflict_sends.count() > 0 ):
                return render(request, 'sorry.html', 
                              {'send_list': conflict_sends.order_by('-timestamp')})

            # TODO actually send freicoins and take the real tx id
            send.tx_id = "0dc2d74db5fddd4f2100f4d99090a2a317f94ed6de17066d366d72ede8336ca4"
            send.save()

            return HttpResponseRedirect('/faucet/recent/')
    else:
        form = forms.FaucetForm()

    return render(request, 'faucet.html', {'form': form})
