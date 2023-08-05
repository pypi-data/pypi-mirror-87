from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def home(request):
    context = {
        'loggedIn': False
    }
    if request.user.is_authenticated:
        context['loggedIn'] = True
   
    return render(request, 'pages/home.html', context)





