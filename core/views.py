from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from core.services.tableService import tableService
from core.services.roundService import roundService

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
            return redirect("signin")

    return render(request, "core/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("signin")

def dashboard(request):
    if request.POST.get("round") is not None:
        table = tableService.getTable()

        name = request.POST.get("name")
        roundNumber = request.POST.get("round")
        
        if(request.POST.get("previous")) :
            roundNumber = str(int(roundNumber)-1)
        else :
            roundNumber = str(int(roundNumber)+1)

        round = roundService.getRound(f'Regular Season - {roundNumber}')

        context= {
                'name': name,
                'roundNumber': roundNumber,
                'round': round,
                'table': table,
                }
        return render(request, "insights/dashboard.html", context)
    
    table = tableService.getTable()

    json = roundService.getJsonRound()

    name = "Campeonato Brasileiro"
    roundNumber = json['response'][0].split(" - ",1)[1]

    round = roundService.getRound(json['response'][0])

    context= {
            'name': name,
            'roundNumber': roundNumber,
            'round': round,
            'table': table,
            }
    return render(request, "insights/dashboard.html", context)