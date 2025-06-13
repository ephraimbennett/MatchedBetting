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

    #bm = BookMaker.objects.get(title="BetRivers")
    #print(bm.states.all())

    
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
        #update_bets()
        bm = request.GET.get('bookmaker')
        if bm != 'Any':
            bets = BonusBet.objects.filter(bonus_bet__contains=bm).order_by("-profit_index")[:int(request.GET.get('limit'))]
        else:
            bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]
        print(len(bets))

        bets_json = []
        bet_list = []
        for bet in bets:
            if not (is_in_state(bet, user_settings.state)):
                continue
                pass
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
            bet_list.append(bet)
            bets_json.append(bet)
        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_bet,
                'bonus_odds': bet.bonus_odds,
                'bonus_name': bet.bonus_name,
                'hedge_bet': bet.hedge_bet,
                'hedge_odds': bet.hedge_odds,
                'hedge_name': bet.hedge_name,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])
        
        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list,
            'bets_json': bets_json, 
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
def site_credit(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    pot_value = 2000 if user_settings.state is None else user_settings.state.value
    bookmakers = BookMaker.objects.all()

    bonus_size = request.GET.get('amount')

    if bonus_size:
        bm = request.GET.get('bookmaker')
        min_odds = request.GET.get('min-odds')
        if bm != 'Any':
            bets = BonusBet.objects.filter(bonus_bet__contains=bm).order_by("-profit_index")[:int(request.GET.get('limit'))]
        else:
            bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]
        print(len(bets))

        bets_json = []
        bet_list = []
        for bet in bets:
            if not (is_in_state(bet, user_settings.state)):
                continue
                pass
            if bet.bonus_odds < int(min_odds):
                continue
            time_adj = bet.time.replace("Z", "+0000")
            dt_utc = datetime.strptime(time_adj, "%Y-%m-%dT%H:%M:%S%z")
            local_time = dt_utc.astimezone(pytz.timezone(user_settings.timezone))
            # Parse the timestamp into a datetime object
            dt = datetime.fromisoformat(str(local_time))
            # Format the datetime object into the desired string
            formatted_time = dt.strftime("%B %d, %Y %I:%M %p")
            bet.time = formatted_time

            # will need to recalculate profit
            s = float(bonus_size)
            odd_b = bet.bonus_odds / 100.0 + 1.0
            odd_h = 100.0 / abs(bet.hedge_odds) + 1.0

            bet.profit_index = s * (odd_b - odd_b / odd_h)
            bet.hedge_index = (s * odd_b) / odd_h
            bet_list.append(bet)
            bets_json.append(bet)
        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_bet,
                'bonus_odds': bet.bonus_odds,
                'bonus_name': bet.bonus_name,
                'hedge_bet': bet.hedge_bet,
                'hedge_odds': bet.hedge_odds,
                'hedge_name': bet.hedge_name,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])
        
        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list,
            'bets_json': bets_json, 
            'settings': user_settings, 
            'bookmakers': bookmakers
            }

        return render(request, 'site_credit.html', vars)

    
    return render(request, 'site_credit.html', {
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
            if not (is_in_state(bet, user_settings.state)):
                continue

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

        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_bet,
                'bonus_odds': bet.bonus_odds,
                'bonus_name': bet.bonus_name,
                'hedge_bet': bet.hedge_bet,
                'hedge_odds': bet.hedge_odds,
                'hedge_name': bet.hedge_name,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])

        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list,
            'bets_json': bets_json,
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
            if not (is_in_state(bet, user_settings.state)):
                continue

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

        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_bet,
                'bonus_odds': bet.bonus_odds,
                'bonus_name': bet.bonus_name,
                'hedge_bet': bet.hedge_bet,
                'hedge_odds': bet.hedge_odds,
                'hedge_name': bet.hedge_name,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])

        vars = {
            'potential_profit': pot_value,
            'bets' : bet_list,
            'bets_json': bets_json,
            'settings': user_settings, 
            'bookmakers': bookmakers
        }

        return render(request, 'profit_boost.html', vars)
            


    return render(request, 'profit_boost.html', {
        'potential_profit': pot_value,
        'settings': user_settings, 
        'bookmakers': bookmakers
    })


states = {
    "AZ": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetFred", "Bally Bet", "Hard Rock", "Sporttrade"],
    "CO": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetFred", "Bally Bet", "Circa Sports", "Sporttrade", "SBK", "BetWildwood"],
    "CT": ["DraftKings", "FanDuel", "Fanatics", "BetRivers"],
    "DC": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET"],
    "IL": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "Circa Sports"],
    "IN": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "Bally Bet", "SBK"],
    "IA": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetFred", "Bally Bet", "Circa Sports", "Hard Rock", "Sporttrade"],
    "KS": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET"],
    "KY": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "Bet365", "Circa Sports"],
    "LA": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "ESPN BET", "BetRivers", "Bet365", "BetFred"],
    "MA": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET"],
    "ME": ["DraftKings", "Caesars"],
    "MD": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bally Bet"],
    "MI": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "BetParx", "Four Winds", "FireKeepers"],
    "NH": ["DraftKings"],
    "NC": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "Underdog Sports"],
    "NJ": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetParx", "Hard Rock", "Sporttrade", "Borgata"],
    "NY": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bally Bet"],
    "OH": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "Hard Rock", "Betly"],
    "OR": ["DraftKings"],
    "PA": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetFred", "BetParx"],
    "TN": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "Bet365", "Betly"],
    "VA": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Bet365", "BetFred", "Bally Bet", "Sporttrade"],
    "VT": ["DraftKings", "FanDuel", "Fanatics"],
    "WV": ["DraftKings", "FanDuel", "BetMGM", "Caesars", "Fanatics", "ESPN BET", "BetRivers", "Betly"],
    "WY": ["FanDuel", "BetMGM"],
    "NV": ["BetMGM", "Caesars", "WynnBet", "Circa Sports", "SuperBook"],
    "FL": ["Hard Rock"],
    "AK": ["Betly"]
}


def is_in_state(bet, state):
    b1 = bet.bonus_bet
    b2 = bet.hedge_bet
    print( (b1 in states[state.code]) and b2 in states[state.code])
    return (b1 in states[state.code]) and b2 in states[state.code]