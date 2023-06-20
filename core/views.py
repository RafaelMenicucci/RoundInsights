import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from django.contrib.auth import authenticate, login, logout
from core.classes.round import Round

from round_insight.settings import TEST_API_KEY_SOCCER
from round_insight.settings import LIVE_API_KEY_SOCCER

# Create your views here.
def home(request):
    return render(request, "core/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            messages.error(request, "Passwords should be the same!")
            return render(request, "core/signup.html")

        myuser = User.objects.create_user(username,'',pass1)
        
        myuser.save()

        messages.success(request, "Your account has been succesfully created.")

        return redirect("signin")

    return render(request, "core/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            return redirect("insights/dashboard")
        else:
            messages.error(request, "Bad credentials!")
            return redirect("home")

    return render(request, "core/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

def dashboard(request):
    # Campeonato Brasileiro
    championship = 10

    headersAuth = {
        'Authorization': 'Bearer '+ str(LIVE_API_KEY_SOCCER),
    }

    # Getting which round is next, or the one that is happening at the moment 
    response = requests.get(f'https://api.api-futebol.com.br/v1/campeonatos/{championship}/', headers=headersAuth)
    json = response.json()

    name = json['nome']
    roundNumber = json['rodada_atual']['rodada']
    
    # Getting informations from the current round
    response = requests.get(f'https://api.api-futebol.com.br/v1/campeonatos/{championship}/rodadas/{roundNumber}', headers=headersAuth)
    json = response.json()

    round = Round(json['nome'],json['rodada'],json['proxima_rodada']['rodada'],json['rodada_anterior']['rodada'],json['partidas'])

    context= {
            'name': name,
            'roundNumber': roundNumber,
            'round': round,
            }
    return render(request, "insights/dashboard.html", context)