from .models import BonusBet, SecondBet, BookMaker, Promo, ProfitBet, State
from .calculator import calculate_all
from datetime import datetime, timezone, timedelta
import json



from django.utils.dateparse import parse_datetime

from .scrape.sportsbookreview import scrape_sportsbookreview
from .scrape.states import scrape_states

import requests

def update_bets():
    # clear existing tables
    SecondBet.objects.all().delete()
    BonusBet.objects.all().delete()
    ProfitBet.objects.all().delete()

    # get the data, will change later obviously
    key_api = "1fcbe0cddc5a8bbf56e301cb2a949d4a"
    url_sports = f"https://api.the-odds-api.com/v4/sports?apiKey={key_api}"
    domain = "https://api.the-odds-api.com/v4/sports/"
    response = requests.get(url=url_sports)
    sports_names = response.json()
    keys = []

    current_date_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    seven_days_later = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7)
    seven_days_later_iso = seven_days_later.strftime('%Y-%m-%dT%H:%M:%SZ')

    for item in sports_names:
        keys.append(item['key'])

    sports = []
    for key in keys:
        url = f"{domain}{key}/events"
        response = requests.get(url, params={
            'sport': key,
            'apiKey': key_api,
            'commenceTimeFrom': current_date_iso,
            'commenceTimeTo': seven_days_later_iso
        })
        if len(response.json()) > 0:
            sports.append(key)

    # get main lines
    
    markets = "h2h,spreads,totals"
    bookmakers = "fanduel,betmgm,betrivers,betus,betrivers,ballybet,draftkings,espnbet,hardrockbet"
    

    data = []
    for key in sports:
        url = f"{domain}{key}/odds"
        response = requests.get(url, params={
            'regions': 'us',
            'oddsFormat': 'american',
            'apiKey': key_api,
            'markets': markets,
            'bookmakers': bookmakers,
            'commenceTimeFrom': current_date_iso,
            'commenceTimeTo': seven_days_later_iso
        })

        data.extend(response.json())
    
    print(json.dumps(data))
    
    bets, second_bets, profit_bets = calculate_all(data)

    # have a set of the names of bookmakers, as we go through the bets, add to this set.
    bookmakers = set()

    print(len(bets))
    for bet in bets:
        bookmakers.add(bet['bonus_bet'][0])
        bookmakers.add(bet['hedge_bet'][0])

        bet_model = BonusBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.hedge_index = bet['hedge_bet'][3]
        bet_model.profit_index = bet['profit_index']
        bet_model.hedge_name = bet['hedge_bet'][2]
        bet_model.bonus_name = bet['bonus_bet'][2]
        bet_model.market = bet['market']
        bet_model.sport = bet['sport']
        bet_model.time = bet['time']

        bet_model.save()

    for bet in second_bets:
        bookmakers.add(bet['bonus_bet'][0])
        bookmakers.add(bet['hedge_bet'][0])

        bet_model = SecondBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.bonus_name = bet['bonus_bet'][2]
        bet_model.hedge_name = bet['hedge_bet'][2]
        bet_model.profit_index = bet['profit_index']
        bet_model.market = bet['market']
        bet_model.sport = bet['sport']
        bet_model.time = bet['time']

        bet_model.save()
    for bet in profit_bets:
        bet_model = ProfitBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.bonus_name = bet['bonus_bet'][2]
        bet_model.hedge_name = bet['hedge_bet'][2]
        bet_model.profit_index = bet['profit_index']
        bet_model.market = bet['market']
        bet_model.sport = bet['sport']
        bet_model.time = bet['time']

        bet_model.save()

    for b in bookmakers:
        book_model = BookMaker(title=b)
        book_model.save()
    print("All bets have been updated.")

def update_promos():
    # clear existing promos
    Promo.objects.all().delete()

    url = "https://www.sportsbookreview.com/bonuses/"
    promos = scrape_sportsbookreview(url)

    for promo in promos:
        model = Promo(bookmaker=promo[0], description=promo[1], code=promo[2])
        if len(promo) == 4:
            model.url = promo[3]
        else:
            model.url = '/'
        model.save()

def update_states():
    # clear existing states
    State.objects.all().delete()

    url = "https://about.darkhorseodds.com/guides/state-guide-overview"
    states = scrape_states(url)

    for state in states:
        model = State(code=state['abbrev'], name=state['name'], value=state['value'])
        model.save()

def print_smg():
    print("SMGSMGSMG\n\nSMHG\nde")