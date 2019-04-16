from django import forms
from .models import BraFitting


class BraFittingForm(forms.ModelForm):

    class Meta:
        model = BraFitting
        fields = ('bra_size', 'band_measurement', 'band_size', 'bust_measurement', 'cup_size', 'bust_circumference')