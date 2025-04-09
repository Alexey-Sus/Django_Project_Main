from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def contact_details(request):
    return render(request, 'contact_details.html')
