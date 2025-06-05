import requests
import json

def get_data():
    url = "https://api.sportsgameodds.com/v2/events/"
    api_key = "0b970343a667aa7b8dfb5142e95099c7"
    headers = {
        'X-Api-Key' : api_key
    }

    params = {
        'leagueID': 'NBA',
        'limit': 1
    }

    response = requests.get(url, headers=headers, params=params) 
    print(json.dumps(response.json(), indent=4))

get_data()