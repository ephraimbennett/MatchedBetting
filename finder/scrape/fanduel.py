from playwright.sync_api import sync_playwright
import re
import json


def scrape_fanduel_domestic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use `False` to see browser UI
        page = browser.new_context(java_script_enabled=True).new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")  # Wait until all network requests settle

        # grab all the links to each event's own parge
        event_links = page.locator("span[role='link'][aria-label]", has_text="More wagers").all()
        urls = [span.locator("xpath=ancestor::a").get_attribute("href") for span in event_links]
        titles = [url.split('/')[-1] for url in urls] # turn the urls into titles for the events
        buttons = page.locator("div[role='button'][aria-label]").all() # every button that has info for a bet

        # this is functionally looping through each event
        sides = []
        for title in titles:
            sides.append(create_sides(title, buttons))
        titles.clear()
        titles = [a + " @ " + b for a, b in sides]
        
        # sort the buttons into their respective events
        aria_values = [] # simply the values from each button
        events = {} # the dictionary we use to store all the dat
        for title in titles:
            events[title] = {} # add each event to the data
        for button in buttons:
            aria_values.append(button.get_attribute("aria-label")) # store the aria_labels
        for val in aria_values:
            # each value is split into multiple sections by a comma to determine data
            val = val.lower()
            sections = val.split(',')

            # this button label would not be for an actual bet
            if len(sections) < 3:
                continue

            # trim the whitespace
            sections = [x.strip() for x in sections]
            team = sections[1]

            # check which event this aria-label belongs to 
            for title in titles:
                if title.find(team.lower()) != -1:
                    # once we find, append the data
                    # it goes: event->bet type->team->odds/data
                    if sections[0] in events[title]:
                        events[title][sections[0]][team] = sections[2:]
                    else:
                        events[title][sections[0]] = {team: sections[2:]}           
        print(page.title())  # Print page title as a test
        browser.close()

        return events
def create_sides(title, buttons):
    # create sides
    sides = title.split('-@-', 1)
    sides[1] = "-".join(sides[1].split('-')[:-1])
    sides = [team.replace('-', ' ') for team in sides]
    return sides

def scrape_fanduel_int(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use `False` to see browser UI
        page = browser.new_context(java_script_enabled=True).new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")  # Wait until all network requests settle


        print(page.title())  # Print page title as a test
        browser.close()
url = "https://sportsbook.fanduel.com/navigation/ncaab"
data = scrape_fanduel_domestic(url)

with open('data/fanduel.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)