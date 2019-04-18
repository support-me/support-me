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
            fitting.save(
                currently_wearing=data['currently_wearing'],
                band_measurement=data['band_measurement'],
                bust_measurement=data['bust_measurement'],
                bust_circumference=data.get('bust_circumference', False),
            )
            fitting_id = fitting.id
            return redirect(f'suggestion-form/{fitting_id}')

    else: 
        form = BraFittingForm()
    
    return render(request , 'bra_fitting.html', {'form': form},)
    
def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request, fitting_id):
    fitting = BraFitting.objects.get(id=fitting_id)

    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            data = form.data
            suggestion.save(
                breast_symmetry=data['breast_symmetry'],
                breast_tissue=data['breast_tissue'],
                breast_placement=data['breast_placement'],
                bra_wire=data.get('bra_wire', False)
            )
            return render(request, 'suggestion-form.html', {'form': suggestion_form , 'bra_size': fitting.bra_size})
    else:
        form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form , 'bra_size': fitting.bra_size})
