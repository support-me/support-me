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
            data = form.data
            context = {}
            
            band_measurement = data['band_measurement']
            bust_measurement = data['bust_measurement']
            bust_circumference = data.get('bust_circumference', False)
            if not bust_circumference:
                band_measurement = int(band_measurement) * 2
                bust_measurement = int(bust_measurement) * 2 
            context['band_measurement'] = band_measurement
            context['bust_measurement'] = bust_measurement
            print(context)
            return HttpResponseRedirect(reverse('brafitting'), context)
    else: 
        form= BraFittingForm()
    return render(request , 'bra_fitting.html', {'form': form})
    
def BraCare(request):
    return render(request, 'bra_care.html')
    
