from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

from apps.faucet.models import *
from apps.faucet import forms

def recent_sends(request):
    sends = FaucetSend.objects.order_by('-timestamp')[:20]
    return render(request, 'recent_sends.html', {'send_list': sends})

def faucet(request):
    if request.method == 'POST':
        form = forms.FaucetForm(request.POST)

        if form.is_valid():

            send = FaucetSend()
            send.frc_address = form.cleaned_data['frc_address']
            send.ip_address = request.META['REMOTE_ADDR']
            # TODO validate, actually send freicoins and take the real tx id
            send.tx_id = "0dc2d74db5fddd4f2100f4d99090a2a317f94ed6de17066d366d72ede8336ca4"
            send.save()

            return HttpResponseRedirect('/faucet/')
    else:
        form = forms.FaucetForm()

    return render(request, 'faucet.html', {'form': form})
