from django.shortcuts import render

def faucet(request):
    return render(request, 'faucet.html')

def recent_sends(request):
    return render(request, 'recent_sends.html')

