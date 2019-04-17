from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def BraCare(request):
    return render(request, 'bra_care.html')
    