from django.shortcuts import render
from core.models import BraFitting
from core.forms import BraFittingForm
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def braFitting(request):
    if request.method == 'POST':
        form = BraFittingForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('brafitting'))
    else: 
        form= BraFittingForm()
    return render(request , 'bra_fitting.html', {'form': form})