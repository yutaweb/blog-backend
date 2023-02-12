from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article

def index(request):
    objs = Article.objects.all()[:3]
    context = {
        'title': 'toyama',
        'articles': objs,
    } 
    return render(request, 'mysite/index.html', context)
