from django import forms
from .models import BraFitting


class BraFittingForm(forms.ModelForm):

    class Meta:
        model = BraFitting
        fields = ('band_measurement', 'bust_measurement', 'bust_circumference')