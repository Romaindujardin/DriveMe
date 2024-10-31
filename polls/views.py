from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.") #On a crée la vue index() qui renvoie un message de salutation.

def hello(request):
    return render(request ,'hello.html') #On a crée la vue hello() qui renvoie un template hello.html dans polls