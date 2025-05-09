from playwright.sync_api import sync_playwright
import re
import json
import time

def scrape_betmgm_domestic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use `False` to see browser UI
        page = browser.new_context(java_script_enabled=True).new_page()
        page.goto(url)

        page.wait_for_selector("ms-six-pack-event")
        time.sleep(0.01) # pause to make sure all the events load
        
        events = {}
        event_elements = page.locator('ms-six-pack-event').all()
        print(len(event_elements))
        for element in event_elements:
            team_group = element.locator('ms-event-detail')
            divs = team_group.locator('div.participant, div.participant.ng-star-inserted').all()
            sides = [div.text_content().lower().strip() for div in divs]

            # so there should be three ms-option-group elements, in the order of:
            # spread, total, moneyline
            # each group's "button" is ms-option. They should correlate to the order of the sides. ie. b0 to side 0
            groups = element.locator('ms-option-group').all()
            
            # spread first
            spread = {}
            options = groups[0].locator('ms-option').all()
            for i in range(2):
                spread[sides[i]] = options[i].text_content().strip().split()
            
            # now total
            total = {}
            options = groups[1].locator('ms-option').all()
            for i in range(len(options)):
                
                words = options[i].text_content().split()
                if len(words) < 2:
                    continue
                label = 'over' if words[0] == 'O' else 'under'
                total[label] = words[1:]

            # moneyline
            moneyline = {}
            options = groups[2].locator('ms-option').all()
            for i in range(len(options)):
                moneyline[sides[i]] = options[i].text_content()
            
            # create title and append data
            title = sides[0] + ' @ ' + sides[1]
            events[title] = {'spread' : spread, 'total' : total, 'moneyline' : moneyline}

        print(page.title())  # Print page title as a test
        browser.close()
        return events
url = "https://sports.mi.betmgm.com/en/sports/basketball-7/betting/usa-9/ncaa-264"
data = scrape_betmgm_domestic(url)

with open('data/betmgm.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)