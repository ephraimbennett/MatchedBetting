from playwright.sync_api import sync_playwright
import re
import json

def scrape_betrivers_domestic(url, sport):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use `False` to see browser UI
        page = browser.new_page()
        page.goto(url)

        # still use selectors for this for now.
        page.wait_for_selector("article[data-testid^='listview-group']")
        show_more = page.query_selector("button[data-testid='show-more-events-button']")
        try:
            while show_more:
                show_more.click()
                print('clicked show more')
                show_more = page.query_selector("button[data-testid='show-more-events-button']")
        except:
            print("No more button")
        
        # grab the eveents using locators
        events = articles = page.locator("article[data-testid^='listview-group']").all()
        
        json_data = {}

        for event in events:
            try:
                title, data = process_event(event, sport)
                json_data[title] = data
            except Exception as e:
                print(e)
                continue

        print(len(events))
        print(page.title())  # Print page title as a test
        browser.close()

        return json_data
        
def process_event(event, sport):
    event.scroll_into_view_if_needed()
    # the title will be the aria-label of the first child div
    title = event.locator(">*").first.get_attribute("aria-label")

    print(title)


    # this section of code gets each side from the title, and the time
    # if it's a UFC event, we need to handle the title differently
    if sport == 'UFC':
        first, second = title.split('-', 1)
        second = second.split(',')
        sides = [first]
        sides.append(",".join(second[:-2]))
        time = ",".join(second[-2:])
        sides = [item.strip() for item in sides]
    else:
        teams, time = title.split(",", 1)
        sides = teams.split("@")
        sides = [item.strip() for item in sides]

    

    # the main lines for the event that we are extracting
    moneyline = {}
    spread = {}
    total = {}

    # grab all the buttons - the aria label of these contains the info we need
    buttons = event.locator("button").all()
    for button in buttons:
        text = button.get_attribute("aria-label")
        if text is None:
            continue
        text = text.lower()
        # first, point spread
        if text.find("Point Spread") != -1:
            # the aria text of the spread is formatted like this:
            # Point Spread, (9) Michigan State -11.5 at -108

            # behind the comma is just the name of the bet, so grab the second half and split into words
            second_words = text.split(",")[1].split(" ") 

            # line will alwasy be the third word from the end 
            line = second_words[-3]
            odds = second_words[-1]

            # this just finds the name of side in the entire text
            if text.find(sides[0]) != -1:
                side = sides[0]
            else:
                side = sides[1]
            spread[side] = [line, odds]

        # now, the moneyline
        if text.find("Moneyline") != -1:
            # process differently for ufc because of the nameing 
            if sport == 'UFC':
                side, odds = process_aria_ufc(text, sides)
                moneyline[side] = odds
                continue

            # the aria text for the moneyline should be formatted like this:
            # Moneyline, Northwestern State at +255

            # behind the comma is just the name of the bet, so grab the second half and split into words
            second_words = text.split(",")[1].split(" ")
            
            # the odds will be the last word
            odds = second_words[-1]
            
            # now find the side by trying to match with one of them
            if text.find(sides[0]) != -1:
                side = sides[0]
            else:
                side = sides[1]
            moneyline[side] = odds
        
        # finally, the total points
        if text.find("Total Points") != -1:
            # the format for this aria text should be like this:
            # Total Points, over 146 at -124
            

            # behind the comma is just the name of the bet, so grab the second half and split into words
            second_words = text.split(",")[1].split(" ")

            # classify if over or under - fourth word from the end
            type = second_words[-4]

            # the line will be the third word from the end
            line = second_words[-3]

            # odds will be the last word
            odds = second_words[-1]
            total[type] = [line, odds]
    data = {'sides': sides, 'moneyline': moneyline, 'spread': spread, 'total': total, 'time': time}

    return title, data

def process_aria_ufc(text, sides):
    odds = text.split()[-1]
    if text.find(sides[0]) != -1:
        side = sides[0]
    else:
        side = sides[1]
    return [side, odds]


url = "https://mi.betrivers.com/?page=sportsbook&group=1000093654&type=matches"
data = scrape_betrivers_domestic(url, 'NCAAW')

with open('data/betrivers.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)