from django import forms
from django.forms import ModelForm
from core.models import User, Profile, BraFitting, Suggestion
from django.core.exceptions import ValidationError

class SuggestionForm(forms.ModelForm):
    """
    Form to ask user questions and then generate suggested bra type
    """
    class Meta:
        model = Suggestion
        fields = ('breast_symmetry', 'breast_tissue', 'breast_placement', 'bra_wire')
