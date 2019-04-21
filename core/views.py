from django.shortcuts import render
from core.models import BraFitting, Suggestion, Resource, Profile
from core.forms import BraFittingForm, SuggestionForm
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers import UserSerializer, GroupSerializer, ProfileSerializer, FittingSerializer
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.
def home(request):
    return render(request, 'index.html')

def braFitting(request):
    if request.method == 'POST':
        form = BraFittingForm(request.POST)
        if form.is_valid():
            # user = BraFitting.user
            fitting = form.save(commit=False)
            data = form.data
            fitting.save(
                # user=user,
                currently_wearing=data['currently_wearing'],
                band_measurement=data['band_measurement'],
                bust_measurement=data['bust_measurement'],
                bust_circumference=data.get('bust_circumference', False),
            )
            fitting_id = fitting.id
            return redirect(f'suggestion-form/{fitting_id}')

    else: 
        form = BraFittingForm()
    
    return render(request, 'bra_fitting.html', {'form': form},)
    
def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request, fitting_id):
    fitting = BraFitting.objects.get(id=fitting_id)

    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            data = form.cleaned_data
            suggestion.save(
                breast_shape=data['breast_shape'],
                bra_padding=data['bra_padding'],
            )
            suggestion_id = suggestion.id
            print(suggestion.bra_suggestion)
            return redirect(f'suggestion-form/{fitting_id}/{suggestion_id}')
    else:
        form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form , 'bra_size': fitting.bra_size})

def results(request, fitting_id, suggestion_id):
    fitting = BraFitting.objects.get(id=fitting_id)
    suggestion = Suggestion.objects.get(id=suggestion_id)
    return render(request, 'results.html', {'bra_size': fitting.bra_size, 'bra_suggestion': suggestion.bra_suggestion})


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

@method_decorator(staff_member_required, name='dispatch')
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@method_decorator(staff_member_required, name='dispatch')
class FittingView(APIView):
    """
    API view for all the fittings data from each fitting session
    """
    def get(self, format=None):
        # user = BraFitting.user
        fitting = BraFitting.objects.all()
        serializer = FittingSerializer(fitting, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates Profile record
        """
        serializer = FittingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(staff_member_required, name='dispatch')
class ProfileView(APIView):
    """
    API view for creating and fetching Profile records
    """
    def get(self, format=None):
        """
        Get all the profile records
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Creates Profile record
        """
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
