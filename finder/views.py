from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Settings, BonusBet, SecondBet, BookMaker, Promo
from .services import update_bets, update_promos, update_states
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
import json

from .forms import SettingsForm


# Create your views here.

@login_required
def dashboard(request):

    bm = BookMaker.objects.get(title="BetRivers")
    print(bm.states.all())

    
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    
    pot_value = 2000 if user_settings.state is None else user_settings.state.value
    
    #update_promos()
    promos = Promo.objects.all()
    print("hhheey")


    return render(request, "dashboard.html", {
        'potential_profit': pot_value,
        'settings': user_settings,
        'promos': promos
    })

@login_required
def settings(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SettingsForm(instance=user_settings)
    return render(request, 'settings.html', {'form' : form})

@login_required
def coming_soon(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    pot_value = 2000 if user_settings.state is None else user_settings.state.value
    return render(request, "coming_soon.html", {'potential_profit': pot_value, 'settings': user_settings})

@login_required
def bonus_bets(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    pot_value = 2000 if user_settings.state is None else user_settings.state.value
    bookmakers = BookMaker.objects.all()

    bonus_size = request.GET.get('amount')
    if bonus_size is not None:

        bm = request.GET.get('bookmaker')
        if bm != 'Any':
            bets = BonusBet.objects.filter(bonus_bet__contains=bm).order_by("-profit_index")[:int(request.GET.get('limit'))]
        else:
            bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]
        print(len(bets))
        for bet in bets:

            time_adj = bet.time.replace("Z", "+0000")
            dt_utc = datetime.strptime(time_adj, "%Y-%m-%dT%H:%M:%S%z")
            local_time = dt_utc.astimezone(pytz.timezone(user_settings.timezone))
            # Parse the timestamp into a datetime object
            dt = datetime.fromisoformat(str(local_time))
            # Format the datetime object into the desired string
            formatted_time = dt.strftime("%B %d, %Y %I:%M %p")
            bet.time = formatted_time

            bet.profit_index *= float(bonus_size)
            bet.hedge_index *= float(bonus_size)

        
        vars = {
            'potential_profit': pot_value,
            'bets' : bets, 
            'settings': user_settings, 
            'bookmakers': bookmakers
            }

        return render(request, 'bonus_bets.html', vars)

    return render(request, 'bonus_bets.html', {
        'potential_profit': pot_value,
        'settings': user_settings, 
        'bookmakers': bookmakers
    })

@login_required
def second_chance(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    bookmakers = BookMaker.objects.all()
    pot_value = 2000 if user_settings.state is None else user_settings.state.value

    second_size = request.GET.get('amount')
    if second_size is not None:

        # grab the S and r from the client.
        S = float(second_size)
        r = float(request.GET.get('return')) / 100.0
        # grab the bookmaker
        bm = request.GET.get('bookmaker')

        # we want to grab the first 500 bets, because we don't know how profitable they really are yet. 
        bets = SecondBet.objects.all().filter(bonus_bet__contains=bm).order_by("-profit_index")[:500]
        bet_list = []
        for bet in bets:
            time_adj = bet.time.replace("Z", "+0000")
            dt_utc = datetime.strptime(time_adj, "%Y-%m-%dT%H:%M:%S%z")
            local_time = dt_utc.astimezone(pytz.timezone(user_settings.timezone))
            # Parse the timestamp into a datetime object
            dt = datetime.fromisoformat(str(local_time))
            # Format the datetime object into the desired string
            formatted_time = dt.strftime("%B %d, %Y %I:%M %p")
            bet.time = formatted_time


            # H = (Ob * S - S * r) / Oh,
            # P = Ob * S - S - (Ob * S - S * r) / Oh
            odd_h = 1 + 100 / abs(bet.hedge_odds)
            odd_b = 1 + bet.bonus_odds / 100
            hedge = (odd_b * S - S * r) / odd_h
            profit = odd_b * S - S - hedge

            bet.profit_index = profit
            bet.hedge_index = hedge
            bet_list.append(bet)
             
        # sort the bets by how much profit and then return the amount wanted to the user
        bet_list.sort(key = lambda bet : bet.profit_index, reverse=True)
        bet_list = bet_list[:int(request.GET.get('limit'))]

        

        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list, 
            'settings': user_settings, 
            'bookmakers': bookmakers
        }
        return render(request, 'second_chance.html', vars)

    return render(request, 'second_chance.html', {
        'potential_profit': pot_value,
        'settings': user_settings, 
        'bookmakers': bookmakers
    })

@login_required
def prompt_action(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    if request.user.is_superuser:
        if request.method == 'POST':
            tasks = json.loads(request.body)['tasks']
            if "update_bets" in tasks:
                update_bets()
            if "update_promos" in tasks:
                update_promos()
        return render(request, 'prompt.html')
    return redirect('/')

@login_required
def profit_boost(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    bookmakers = BookMaker.objects.all()
    pot_value = 2000 if user_settings.state is None else user_settings.state.value
    

    bonus_size = request.GET.get('amount')

    if bonus_size is not None:
        bm = request.GET.get('bookmaker')
        if bm != 'Any':
            bets = BonusBet.objects.filter(bonus_bet__contains=bm).order_by("-profit_index")[:500]
        else:
            bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]

        # grab the bonus stake and the boost percentage
        stake_b = float(request.GET.get('amount'))
        boost = float(request.GET.get('boost')) / 100.0 + 1.0

        bet_list = []
        for bet in bets:
            # need to calculate the actual profit and then replace the profit index with this
            odd_h = 100 / abs(bet.hedge_odds)
            odd_b = bet.bonus_odds / 100
            bet.profit_index = (odd_b * boost) - (odd_b * boost + 1) / (odd_h + 1) 
            bet.profit_index *= stake_b
            # calculate hedge size as well
            
            bet.hedge_index = stake_b
            bet.hedge_index *= (odd_b * boost + 1) / (odd_h + 1)

            time_adj = bet.time.replace("Z", "+0000")
            dt_utc = datetime.strptime(time_adj, "%Y-%m-%dT%H:%M:%S%z")
            local_time = dt_utc.astimezone(pytz.timezone(user_settings.timezone))
            # Parse the timestamp into a datetime object
            dt = datetime.fromisoformat(str(local_time))
            # Format the datetime object into the desired string
            formatted_time = dt.strftime("%B %d, %Y %I:%M %p")
            bet.time = formatted_time
            bet_list.append(bet)
        bet_list.sort(key = lambda bet : bet.profit_index, reverse=True)
        bet_list = bet_list[:int(request.GET.get('limit'))]
        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list, 
            'settings': user_settings, 
            'bookmakers': bookmakers
        }

        return render(request, 'profit_boost.html', vars)
            


    return render(request, 'profit_boost.html', {
        'potential_profit': pot_value,
        'settings': user_settings, 
        'bookmakers': bookmakers
    })