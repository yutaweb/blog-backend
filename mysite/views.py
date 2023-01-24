from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': 'toyama'
    } 
    return render(request, 'mysite/index.html', context)
