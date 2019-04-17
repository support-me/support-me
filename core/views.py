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
            data = form.data
            band_measurement = data['band_measurement']
            bust_measurement = data['bust_measurement']
            bust_circumference = data.get('bust_circumference', False)  

            # get bust_measurment below
            if not bust_circumference:
                bust_measurement = int(bust_measurement) * 2
            else:
                bust_measurement = int(bust_measurement)

            # get band_size below
            band_measurement_int = math.floor(int(band_measurement))
            if band_measurement_int % 2 == 0:
                band_size = (band_measurement_int + 4)
            else:
                band_size = (band_measurement_int + 5)

            # get cup_size below
            CUP_OPTIONS = {
                0:'AA',
                1:'A',
                2:'B',
                3:'C',
                4:'D',
                5:'DD/E',
                6:'DDD/F',
                7:'G',
                8:'H',
                9:'I',
                10:'J',
                11:'K',
                12:'L',
                13:'M',
            }
            # https://stackoverflow.com/questions/11041405/why-dict-getkey-instead-of-dictkey
            cup_size_number = int(bust_measurement - band_size)
            cup_size = CUP_OPTIONS.get(cup_size_number)
    
            #print brasize
            bra_size = (f'{band_size} {cup_size}')
            context = {
            'cup_size': cup_size,
            'band_measurement': band_measurement,
            'band_size': band_size,
            'bust_measurement': bust_measurement,
            'bra_size': bra_size,
            }
            return HttpResponseRedirect(reverse('brafitting'), context)
    else: 
        form = BraFittingForm()
    
    return render(request , 'bra_fitting.html', {'form': form},)
    
def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request):
    form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form})
