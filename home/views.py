from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from .forms import MemberCreationForm

def home(request):
    return render(request, "home.html")

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {'error' : "Invalid email or password."})
    else:
        template = loader.get_template('login.html')
        return render(request, "login.html")

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        data = {
            'message': 'Successful Logout'
        }
        return JsonResponse(data)
    
def register(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            errors = {}
            print(form.errors.as_text())
            return render(request, 'register.html', {'errors': form.errors.as_text()})
    return render(request, "register.html")

def handler404(request, error):
    print("hah")
    template = loader.get_template('404.html')
    context = {
        'request': request
    }
    
    return HttpResponse(template.render())