from django import forms
from django.forms import ModelForm
from core.models import BraFitting, User, Profile, Suggestion
from django.core.exceptions import ValidationError

class BraFittingForm(forms.ModelForm):

    class Meta:
        model = BraFitting
        

        fields = ('currently_wearing', 'band_measurement', 'bust_measurement', 'bust_circumference')

class SuggestionForm(forms.ModelForm):
    """
    Form to ask user questions and then generate suggested bra type
    """
    class Meta:
        model = Suggestion
        fields = ('breast_symmetry', 'breast_tissue', 'breast_placement', 'bra_padding', 'bra_wire')
