from django import forms
from django.forms import ModelForm
from core.models import BraFitting, User, Profile, Suggestion
from django.core.exceptions import ValidationError

class BraFittingForm(forms.ModelForm):
    """
    Form to get user measurements and return a bra size based on their input.
    """
    class Meta:
        model = BraFitting
        fields = ('currently_wearing', 'band_measurement', 'bust_measurement', 'bust_circumference')
        widgets = {
            'currently_wearing': forms.RadioSelect,
            'bust_circumference': forms.RadioSelect,
        }

class SuggestionForm(forms.ModelForm):
    """
    Form to ask user questions and then generate suggested bra type.
    """
    class Meta:
        model = Suggestion
        fields = ('breast_shape', 'breast_placement', 'bra_padding', 'bra_wire')
        widgets = {
            'breast_shape': forms.RadioSelect,
            'breast_placement': forms.RadioSelect,
            'bra_padding': forms.RadioSelect,
            'bra_wire': forms.RadioSelect,
        }

class DeleteFittingForm(forms.ModelForm):
    """ 
    Form lets the user delete 
    """
    class Meta:
        model = Suggestion
        fields = ('fitting_session',)
