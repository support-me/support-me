from django.shortcuts import render
from core.models import BraFitting
from core.forms import BraFittingForm, SuggestionForm
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse
import math

# Create your views here.
def home(request):
    return render(request, 'index.html')

def braFitting(request):
    if request.method == 'POST':
        form = BraFittingForm(request.POST)
        if form.is_valid():
            fitting = form.save(commit=False)
            data = form.data
            # fitting.band_size = band_size
            # fitting.bra_size = bra_size
            # fitting.cup_size = cup_size
            fitting = fitting.save(
                band_measurement=data['band_measurement'],
                bust_measurement=data['bust_measurement'],
                bust_circumference=data.get('bust_circumference', False),
            )
            context = {
                'fitting': fitting,
            }
            return HttpResponseRedirect(reverse('suggestion-form'), context)
    else: 
        form = BraFittingForm()
    
    return render(request , 'bra_fitting.html', {'form': form},)
    
def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request):
    form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form})
