from playwright.sync_api import sync_playwright
import re

def scrape_sportsbookreview(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use `False` to see browser UI
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("div.table-responsive")

        promos = []

        table_whole = page.locator("table.table-borderedless").first
        table_body = table_whole.locator("tbody")
        rows = table_body.locator("tr").all()
        for row in rows:
            # grab the text 
            tds = row.locator('td').all()
            promo = []
            for td in tds:
                promo.append(td.inner_text())

            # grab the url
            a = row.locator('a').first
            if a :
                promo.append(a.get_attribute('href'))

            promos.append(promo)

        return promos