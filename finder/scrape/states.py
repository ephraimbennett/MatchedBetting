from playwright.sync_api import sync_playwright
import re

state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "DC": "DC",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Ontario": "ON",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}


def scrape_states(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use `False` to see browser UI
        context = browser.new_context()
        page = browser.new_page()
        page.goto(url)
        
        # grab the table then the rows
        table_whole = page.locator('table[fs-richtext-component="state-table-overview"]')
        table_whole.wait_for(state='visible')
        rows = table_whole.locator('tbody').locator('tr').all()

        states = []
        for row in rows:
            # grab the cells
            cells = row.locator('td').all()
            
            # index 0 is state name and index 2 is "sign-up value"
            name = cells[0].inner_text()
            value = int(cells[2].inner_text()[1:].replace(",", ""))

            states.append({'name': name, 'abbrev': state_to_abbrev[name], "value": value})
        return states
    