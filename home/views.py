from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model



from google.oauth2 import id_token
from google.auth.transport import requests

import os


from .forms import MemberCreationForm

def home(request):
    return render(request, "new.html")

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {
                'errors' : "Invalid email or password.",
                'email': email
            })
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
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/settings')
        else:
            errors = {}
            print(form.errors.as_text())
            return render(request, 'signup.html', {
                'errors': form.errors.as_text(),
                'email': request.POST.get('email')
            })
    return render(request, "signup.html")

def handler404(request, error):
    print("hah")
    template = loader.get_template('404.html')
    context = {
        'request': request
    }
    
    return HttpResponse(template.render())

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST.get('credential')
    if not token:
        return HttpResponse("Missing token", status=400)

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # Save any new user to the database.
    # You could also authenticate the user here using the details from Google 
    # (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)

    email = user_data.get("email")
    first_name = user_data.get("given_name", "")
    last_name = user_data.get("family_name", "")

    User = get_user_model()
    user, created = User.objects.get_or_create(email=email, defaults={
        "email" : email
    })
    login(request, user)

    return redirect('/')