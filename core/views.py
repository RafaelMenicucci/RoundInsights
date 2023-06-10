import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from django.contrib.auth import authenticate, login, logout

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
    headersAuth = {
        'Authorization': 'Bearer '+ str(TEST_API_KEY_SOCCER),
    }

    response = requests.get('https://api.api-futebol.com.br/v1/campeonatos', headers=headersAuth)
    json = response.json()
    return render(request, "insights/dashboard.html")