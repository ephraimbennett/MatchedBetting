from .models import Event, Line

def find_events(data):
    events = []
    for event in data:
        # check to see if there are even any bookmakers
        if not isinstance(event, dict):
            continue

        if len(event['bookmakers']) == 0:
            print("this happens")
            continue
        lines = []
        skip = False
        # now, check each bookmaker
        for bookie in event['bookmakers']:
            if len(bookie['markets'][0]['outcomes']) > 2:
                skip = True
                continue
            for outcome in bookie['markets'][0]['outcomes']:
                lines.append({'price': outcome['price'], 'side': outcome['name'], 'bookmaker': bookie['title']})
        if skip:
            continue
        to_add = {
                'lines': lines,
                'title': event["away_team"] + " @ " + event["home_team"],
                'time' : event['commence_time'],
                'sport': event['sport_title']
        }
        # try to add the type of event, ie market
        try:
            val = event['bookmakers'][0]['markets'][0]['key']
            to_add['market'] = 'Moneyline' if val == 'h2h' else val
        except Exception as e:
            print(e)

        events.append(to_add)
    return events

def derive_bets(bookmaker, state):
    bets = []
    events = Event.objects.prefetch_related('lines').all()
    i = 0
    for e in events:
        bet = {
            'bonus_side': [],
            'hedge_side': []
        }
        if len(bookmaker) == 0:
            sides = {}
            
        for line in e.lines.all():
            i += 1
            if line.bookmaker not in states[state.code]:
                continue
            if line.bookmaker == bookmaker and line.odds > 0:
                bet['bonus_side'].append(line)
            else:
                bet['hedge_side'].append(line)
            if len(bookmaker) == 0:
                sides.setdefault(line.side, []).append(line)
                
        bet['bonus_side'].sort(key= lambda l : l.odds, reverse=True)
        bet['hedge_side'].sort(key= lambda l : l.odds, reverse=True)
        if len(bookmaker) == 0: 
            if len(sides) < 2: continue

            skip = False
            side_names = list(sides.keys())

            for side in sides.values():
                if len(side) == 0:
                    skip = True
                side.sort(key=lambda l : l.odds, reverse=True)
            if skip: continue
            
            

            if sides[side_names[0]][0].odds > 0:
                b_line = sides[side_names[0]][0]
                h_line = sides[side_names[1]][0]
            else:
                b_line = sides[side_names[1]][0]
                h_line = sides[side_names[0]][0]
            e.bonus_line = b_line
            e.hedge_line = h_line

        else:
            if len(bet["bonus_side"]) == 0 or len(bet['hedge_side']) == 0:
                continue
            idx = 0
            while bet['bonus_side'][0].side == bet['hedge_side'][idx].side:
                idx += 1
            print("For this event", e.title, "the best lines are: ")
            print(bet['bonus_side'][0].side, bet['bonus_side'][0].odds)
            print(bet['hedge_side'][idx].side, bet['hedge_side'][idx].odds)
            e.bonus_line = bet['bonus_side'][0]
            e.hedge_line = bet['hedge_side'][idx]
        bets.append(e)
        
    print(i)
    return bets

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