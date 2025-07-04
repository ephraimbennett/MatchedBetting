from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Settings, BonusBet, SecondBet, BookMaker, Promo
from .services import update_bets, update_promos, update_states, update_events
from .events import derive_bets
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

    for promo in promos:
        if promo.code != "No code required":
            promo.code = "Check for code in terms and conditions"

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

def shared_finder_context(settings):
    
    pot_value = 2000 if settings.state is None else settings.state.value
    bookmakers = BookMaker.objects.all()
    return {
        'potential_profit': pot_value,
        'settings': settings, 
        'bookmakers': bookmakers
    }

@login_required
def bonus_bets(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    context = shared_finder_context(user_settings)

    bonus_size = request.GET.get('amount')
    if bonus_size is not None:

        bm = request.GET.get('bookmaker')
        bets_json = []
        bet_list = []
        bets = derive_bets(bm, user_settings.state)
        for bet in bets:
            
            dt_utc = datetime.strptime(bet.time, "%Y-%m-%dT%H:%M:%S%z")
            user_tz = pytz.timezone(user_settings.timezone)
            dt_local = dt_utc.astimezone(user_tz)
            formatted_time = dt_local.strftime("%B %d, %Y %I:%M %p")

            bet.time = formatted_time
            
            # calculate profit
            # profit = S x (Ob - 1) x ((Oh - 1) / Oh)
            s = float(bonus_size)
            odd_b = bet.bonus_line.odds / 100.0 + 1.0
            odd_h = 100.0 / abs(bet.hedge_line.odds) + 1.0

            bet.profit_index = s * (odd_b - 1) * ((odd_h - 1) / odd_h)
            bet.hedge_index = s * ((odd_b - 1) / odd_h)
            bet_list.append(bet)
            bets_json.append(bet)
        bet_list.sort(key = lambda bet : bet.profit_index, reverse=True)
        bet_list = bet_list[:int(request.GET.get('limit'))]
        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_line.bookmaker,
                'bonus_odds': bet.bonus_line.odds,
                'bonus_name': bet.bonus_line.side,
                'hedge_bet': bet.hedge_line.bookmaker,
                'hedge_odds': bet.hedge_line.odds,
                'hedge_name': bet.hedge_line.side,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])
        
        vars = {
            'bets' : bet_list,
            'bets_json': bets_json
        }

        context.update(vars)

    return render(request, 'bonus_bets.html', context)

@login_required
def site_credit(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    context = shared_finder_context(user_settings)

    bonus_size = request.GET.get('amount')

    if bonus_size:
        bm = request.GET.get('bookmaker')
        min_odds = request.GET.get('min-odds')
        bets = derive_bets(bm, user_settings.state)

        bets_json = []
        bet_list = []
        for bet in bets:
            if bet.bonus_line.odds < int(min_odds):
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
            odd_b = bet.bonus_line.odds / 100.0 + 1.0
            odd_h = 100.0 / abs(bet.hedge_line.odds) + 1.0

            bet.profit_index = s * (odd_b - odd_b / odd_h)
            bet.hedge_index = (s * odd_b) / odd_h
            bet_list.append(bet)
            bets_json.append(bet)
        bet_list.sort(key= lambda bet : bet.profit_index, reverse=True)
        bet_list = bet_list[:int(request.GET.get('limit'))]
        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_line.bookmaker,
                'bonus_odds': bet.bonus_line.odds,
                'bonus_name': bet.bonus_line.side,
                'hedge_bet': bet.hedge_line.bookmaker,
                'hedge_odds': bet.hedge_line.odds,
                'hedge_name': bet.hedge_line.side,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])
        
        vars = {
            'bets' : bet_list,
            'bets_json': bets_json
        }
        context.update(vars)
    
    return render(request, 'site_credit.html', context) 

@login_required
def second_chance(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    context = shared_finder_context(user_settings)

    second_size = request.GET.get('amount')
    if second_size is not None:

        # grab the S and r from the client.
        S = float(second_size)
        r = float(request.GET.get('return')) / 100.0
        # grab the bookmaker
        bm = request.GET.get('bookmaker')

        bets = derive_bets(bm, user_settings.state)
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
            odd_h = 1 + 100 / abs(bet.hedge_line.odds)
            odd_b = 1 + bet.bonus_line.odds / 100
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
                'bonus_bet': bet.bonus_line.bookmaker,
                'bonus_odds': bet.bonus_line.odds,
                'bonus_name': bet.bonus_line.side,
                'hedge_bet': bet.hedge_line.bookmaker,
                'hedge_odds': bet.hedge_line.odds,
                'hedge_name': bet.hedge_line.side,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])

        vars = {
            'bets' : bet_list,
            'bets_json': bets_json
        }
        context.update(vars)

    return render(request, 'second_chance.html', context)

@login_required
def prompt_action(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    if request.user.is_superuser:
        if request.method == 'POST':
            tasks = json.loads(request.body)['tasks']
            if "update_bets" in tasks:
                update_events()
            if "update_promos" in tasks:
                update_promos()
        return render(request, 'prompt.html')
    return redirect('/')

@login_required
def profit_boost(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    context = shared_finder_context(user_settings)
    

    bonus_size = request.GET.get('amount')

    if bonus_size is not None:
        bm = request.GET.get('bookmaker')
        bets = derive_bets(bm, user_settings.state)

        # grab the bonus stake and the boost percentage
        stake_b = float(request.GET.get('amount'))
        boost = float(request.GET.get('boost')) / 100.0 + 1.0

        bet_list = []
        for bet in bets:

            # need to calculate the actual profit and then replace the profit index with this
            odd_h = 100 / abs(bet.hedge_line.odds)
            odd_b = bet.bonus_line.odds / 100
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
                'bonus_bet': bet.bonus_line.bookmaker,
                'bonus_odds': bet.bonus_line.odds,
                'bonus_name': bet.bonus_line.side,
                'hedge_bet': bet.hedge_line.bookmaker,
                'hedge_odds': bet.hedge_line.odds,
                'hedge_name': bet.hedge_line.side,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])

        vars = {
            'bets' : bet_list,
            'bets_json': bets_json
        }

        context.update(vars)
            


    return render(request, 'profit_boost.html', context)

@login_required
def qualifying_bet(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    context = shared_finder_context(user_settings)

    bonus_size = request.GET.get('amount')
    if bonus_size is not None:
        bm = request.GET.get('bookmaker')
        r = float(request.GET.get('return')) / 100.0
        bets = derive_bets(bm, user_settings.state)
        print(len(bets))

        bets_json = []
        bet_list = []
        for bet in bets:


            dt_utc = datetime.strptime(bet.time, "%Y-%m-%dT%H:%M:%S%z")
            user_tz = pytz.timezone(user_settings.timezone)
            dt_local = dt_utc.astimezone(user_tz)
            formatted_time = dt_local.strftime("%B %d, %Y %I:%M %p")

            bet.time = formatted_time

            # TBH, only difference is how we calculate these guys.
            odd_h = 100 / abs(bet.hedge_line.odds) + 1
            odd_b = bet.bonus_line.odds / 100 + 1

            stake_b = float(bonus_size)

            print(stake_b, r)
            bet.profit_index = stake_b * (odd_b - (odd_b / odd_h) - 1 + r)
            bet.hedge_index = stake_b * (odd_b / odd_h)
            bet_list.append(bet)
            bets_json.append(bet)

        bet_list.sort(key = lambda bet : bet.profit_index, reverse=True)
        bet_list = bet_list[:int(request.GET.get('limit'))]
        bets_json = json.dumps([
            {
                'title': bet.title,
                'market': bet.market,
                'time': bet.time,
                'sport': bet.sport,
                'bonus_bet': bet.bonus_line.bookmaker,
                'bonus_odds': bet.bonus_line.odds,
                'bonus_name': bet.bonus_line.side,
                'hedge_bet': bet.hedge_line.bookmaker,
                'hedge_odds': bet.hedge_line.odds,
                'hedge_name': bet.hedge_line.side,
                'hedge_index': bet.hedge_index,
                'profit': bet.profit_index
            }
            for bet in bet_list
        ])
        
        vars = {
            'bets' : bet_list,
            'bets_json': bets_json
        }

        context.update(vars)

    return render(request, 'qualifying_bet.html', context)


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
    return (b1 in states[state.code]) and b2 in states[state.code]