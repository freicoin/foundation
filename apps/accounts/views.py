from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

import forms

def register(request):
    # try:
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = forms.RegisterForm()
    # except:
    #     raise Http404()

    return render(request, 'register.html', {'form': form})
