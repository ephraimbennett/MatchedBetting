from datetime import datetime, timezone, timedelta
import json

import requests

def update_bets():

    # get the data, will change later obviously
    key_api = "23e42a8dbf01cd559ff15daf7fbe062f"
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
        print(item)

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

update_bets()