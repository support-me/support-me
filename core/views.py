from django.shortcuts import render
from core.models import BraFitting
from core.forms import BraFittingForm, SuggestionForm
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def braFitting(request):
    if request.method == 'POST':
        form = BraFittingForm(request.POST)
        if form.is_valid():
            data = form.data
            context = {}
            band_measurement = data['band_measurement']
            bust_measurement = data['bust_measurement']
            bust_circumference = data.get('bust_circumference', False)  
            print(band_measurement)
            print(bust_measurement) 
            print(bust_circumference)

            if not bust_circumference:
                bust_measurement = int(bust_measurement) * 2

            else:
                bust_measurement = int(bust_measurement)
            
            context[
                'cup_size': cup_size,
                'band_measurement': band_measurement,
                'bust_measurement': bust_measurement,
            ] 
            print(context)
            return HttpResponseRedirect(reverse('brafitting'), context=context)
    else: 
        form= BraFittingForm()
    return render(request , 'bra_fitting.html', {'form': form})
    
def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request):
    form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form})
