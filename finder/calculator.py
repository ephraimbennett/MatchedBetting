import requests
import json

def calculate_all(data):
    bets = find_best_bets(data)
    print("starting?")

    bonus_bets = bonus_bet_calc(bets)
    second_bets = second_chance_calc(bets)
    print("found second bets")
    profit_bets = profit_boost_calc(bets)

    return bonus_bets, second_bets, profit_bets



def find_best_bets(data):
    bets = []
    for event in data:
        # info needed for the event
        biggest_plus = 0
        bet_bookie = hedge_bookie = ''
        p_name = m_name = ''
        largest_minus = -99999
        # check to see if there are even any bookmakers
        if len(event['bookmakers']) == 0:
            continue

        # now, check each bookmaker
        for bookie in event['bookmakers']:
            for outcome in bookie['markets'][0]['outcomes']:
                # eliminate draws from the outcomes
                if outcome['name'].lower() == 'draw':
                    continue

                if outcome['price'] > 0: # underdog
                    if outcome['price'] > biggest_plus:
                        biggest_plus = outcome['price']
                        bet_bookie = bookie['title']
                        p_name = outcome['name']
                else:
                    if outcome['price'] > largest_minus:
                        largest_minus = outcome['price']
                        hedge_bookie = bookie['title']
                        m_name = outcome['name']
        to_append = {'bonus_bet': [bet_bookie, biggest_plus, p_name], 'hedge_bet': [hedge_bookie, largest_minus, m_name]}
        to_append['title'] = event["away_team"] + " @ " + event["home_team"]
        to_append['time'] = event['commence_time']
        to_append['sport'] = event['sport_title']

        # try to add the type of event, ie market
        try:
            val = event['bookmakers'][0]['markets'][0]['key']
            to_append['market'] = 'Moneyline' if val == 'h2h' else val
        except Exception as e:
            print(e)

        bets.append(to_append)
    return bets

def bonus_bet_calc(bets):
    # we need to find the max profit given the odds of both sides of a bet
    # given these variables:
    # S = bonus bet size, Ob = odds of the bonus, Oh = odds of the hedge (decimal form for both)
    # Profit (P) = S x (Ob - 1) x ((Oh - 1) / Oh)
    # to convert american odds to decimal:
    # for positive odds (+): O = 1 + (odds / 100)
    # for negative odds (-): O = 1 + (100 / odds)
    # this section of the Profit equation ~ (Ob - 1) x ((Oh - 1) / Oh) ~ stays the same for each bet size.
    # we want to maximize this number, so find the largest, Ob and the largest Oh for a given event. 

    # lets iterate through each event, and find the biggest underdog odds, and the smallest favorite odds
    # then we'll calculate the max profit and store it
    bonus_bets = []
    for bet in bets:     
        plus = bet['bonus_bet'][1]
        minus = bet['hedge_bet'][1]

        # calculate the profit index ~ (Ob - 1) x ((Oh - 1) / Oh)
        odd_b = 1 + plus / 100
        odd_h = 1 + (100 / abs(minus))
        profit_idx = (odd_b - 1) * ((odd_h - 1) / odd_h)

        hedge_index = (odd_b - 1) / odd_h
        bet['hedge_bet'].append(hedge_index)
        bonus_bet = {'bonus_bet': bet['bonus_bet'], 'hedge_bet': bet['hedge_bet']}
        bonus_bet['profit_index'] = profit_idx
        bonus_bet['title'] = bet['title']
        bonus_bet['market'] = bet['market']
        bonus_bet['time'] = bet['time']
        bonus_bet['sport'] = bet['sport']

        bonus_bets.append(bonus_bet)
    return bonus_bets

def second_chance_calc(bets):
    '''
    Given, ob = second chance odds, oh = hedge odds, S = second chance size, H = hedge size, r = return find profit:
    P = Ob * S - S - H = Oh * H - H - S + S * r ==>
    H = (Ob * S - S * r) / Oh,
    P = Ob * S - S - (Ob * S - S * r) / Oh


    '''
    second_bets = []
    for bet in bets:
        plus = bet['bonus_bet'][1]
        minus = bet['hedge_bet'][1]


        # Calculate the implied odds
        # this will help
        implied_b = 100 / (plus + 100)
        implied_h = minus / (minus + 100)
        diff = 1 - (implied_b + implied_h)

        second_bet = {'bonus_bet': bet['bonus_bet'], 'hedge_bet': bet['hedge_bet']}
        second_bet['profit_index'] = diff
        second_bet['title'] = bet['title']
        second_bet['market'] = bet['market']
        second_bet['time'] = bet['time']
        second_bet['sport'] = bet['sport']
        second_bets.append(second_bet)
    return second_bets

def profit_boost_calc(bets):
    '''
    P = (Ob - 1) * B * Sb - Sh
    Sh = Sb * (((Ob - 1) * B + 1) / ((Oh - 1) + 1))
    Profit index = (Ob - 1) * ((Ob - 1) + 1) / ((Oh - 1) + 1)
    '''
    profit_bets = []
    for bet in bets:
        plus = bet['bonus_bet'][1]
        minus = bet['hedge_bet'][1]


        # Calculate the decimal odds
        # leaving the + 1 out of the decimal formula since we're just gonna take it out later - saves time
        odd_b = 100 / (plus + 100)
        odd_h = minus / (minus + 100)

        # simply find the profit index - actual profit calculated when serving to user
        profit_idx = odd_b * ((odd_b + 1) / (odd_h + 1)) 
        p_bet = {'bonus_bet': bet['bonus_bet'], 'hedge_bet': bet['hedge_bet']}
        p_bet['profit_index'] = profit_idx
        p_bet['title'] = bet['title']
        p_bet['market'] = bet['market']
        p_bet['time'] = bet['time']
        p_bet['sport'] = bet['sport']
        p_bet['profit_index'] = profit_idx
        profit_bets.append(p_bet)
    return profit_bets

        

