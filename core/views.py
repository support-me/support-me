from django.shortcuts import render
from .forms import SuggestionForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

def BraCare(request):
    return render(request, 'bra-care.html')
    
def suggestion_form(request):
    form = SuggestionForm()
    return render(request, 'suggestion-form.html', {'form': form})
