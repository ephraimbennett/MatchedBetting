from playwright.sync_api import sync_playwright
import re
import json

def scrape_draftkings_domestic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use `False` to see browser UI
        page = browser.new_context(java_script_enabled=True).new_page()
        page.goto(url)
        page.wait_for_selector('div[data-testid="responsive-card-container"]')

        table_head = page.locator('thead.sportsbook-table__head')
        table_body = page.locator('tbody.sportsbook-table__body')
        rows = table_body.locator('tr').all()
        headers = table_head.locator("th").all()
        column_names = [th.text_content().strip() for th in headers]
        print(column_names)

        events = {}

        for i in range(0, len(rows), 2):
            r1 = rows[i]
            r2 = rows[i + 1]

            sides = [r1.locator('div.event-cell__name-text').text_content().lower(), 
                     r2.locator('div.event-cell__name-text').text_content().lower()]
            title = sides[0] + ' @ ' + sides[1]

            moneyline = {}
            spread = {}
            total = {}
            td_1 = r1.locator('td').all()
            td_2 = r2.locator('td').all()
            tds = [td_1, td_2]
            
            # get the spreads
            # for each td for the spread, there should be two spans. The first contains the line, the second the odds
            for i in range(2):
                spans = tds[i][0].locator('span').all()
                if len(spans) < 1: # handles cases where the td is empty
                    break
                spread[sides[i]] = [span.text_content().lower() for span in spans]
            
            # get the total
            # there should be four spans. First is over/under, second is a break, 3rd is line fourth is odds
            for i in range(2):
                spans = tds[i][1].locator('span').all()
                if len(spans) < 1:
                    break
                label = 'over' if spans[0].text_content() == 'O' else 'under'
                total[label] = [spans[2].text_content().lower(), spans[3].text_content().lower()]
            
            # get the moneyline
            # should be just one spread with the odds
            for i in range(2):
                spans = tds[i][2].locator('span').all()
                if len(spans) < 1:
                    break
                moneyline[sides[i]] = spans[0].text_content().lower()

            events[title] = {'spread' : spread, 'total': total, 'moneyline' : moneyline}
            #print(moneyline)

        print(page.title())  # Print page title as a test
        browser.close()

        return events

url = "https://sportsbook.draftkings.com/leagues/basketball/ncaab"

data = scrape_draftkings_domestic(url)

with open('data/draftkings.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)