from django.shortcuts import render
from core.models import BraFitting, Resource
from core.forms import BraFittingForm, SuggestionForm
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from core.serializers import UserSerializer, GroupSerializer
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

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
    form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form, 'bra_size': fitting.bra_size})


def resourcepage(request):
    resources = Resource.objects.all()
    context = {
        'resources': resources
    }
    return render(request, 'resource.html', context=context)

# views for API User and Group
@method_decorator(staff_member_required, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
