import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import player_info
from scrapy.crawler import CrawlerProcess
import re
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright
from NBA.const import COUNTRIES, MONTH_MAP
from datetime import datetime

class NbaScraping(scrapy.Spider):
    name = "info"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium")
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("CONCURRENT_REQUESTS", 100)
        settings.set("DOWNLOAD_DELAY", 0.5)
        settings.set("AUTOTHROTTLE_TARGET_CONCURRENCY", 100)
        settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", 32)

    def start_requests(self):
        start_urls = []

        with open("data/player_urls.jsonl") as file:
            for line in file.read().splitlines():
                post = json.loads(line)
                player_url = post["player_url"]
                start_urls.append(f"https://www.nba.com/{player_url}")

        for url in start_urls:
            yield scrapy.Request(
                url=url, callback=self.parse
            )

    def parse(self, response):
        # soup = BeautifulSoup(response.text, "html.parser")

        # players' name
        name_elements = response.css('div.PlayerSummary_mainInnerBio__JQkoj p.PlayerSummary_playerNameText___MhqC::text').getall()
        first_name = name_elements[0] if name_elements else "N/A"
        last_name = name_elements[1] if len(name_elements) > 1 else "N/A"

        # other player information
        elements = response.css('div.PlayerSummary_playerInfo__om2G4 p.PlayerSummary_playerInfoValue__JS8_v::text').getall()

        qualified_elements = {}

        for ele in elements:
            # find the country
            pattern_country = r"^[A-Za-z]+$"
            if ele and re.match(pattern_country, ele):
                for country in COUNTRIES:
                    if 'country' not in qualified_elements:
                        if ele.lower() == country['name'].lower():
                            qualified_elements['country'] = country['code']
                            break
                        elif ele.lower() == country['code'].lower():
                            qualified_elements['country'] = country['code']  # Store name instead of code
                            break
                else:  # This else belongs to the for loop, not the if statement
                    if 'country' not in qualified_elements:
                        qualified_elements['country'] = 'N/A'

            # find the birth date
            pattern = r"(?i)(January|February|March|April|May|June|July|August|September|October|November|December)\s([1-9]|[12][0-9]|3[01]),\s\d{4}"
            if ele and re.match(pattern, ele):
                if ele not in qualified_elements:
                    qualified_elements['birth'] = ele
                    month, day, year = qualified_elements['birth'].replace(',', '').split()
                    qualified_elements['birth'] = f"{MONTH_MAP[month]}/{day}/{year}"

            # find the draft (full set)
            pattern_draft = r"(\d{4})\sR(\d+)\sPick\s(\d+)"
            if ele and ele.strip():
                match_draft = re.match(pattern_draft, ele)
                if ele == "Undrafted":
                    qualified_elements['draft_year'] = "Undrafted"
                    qualified_elements['draft_round'] = "Undrafted"
                    qualified_elements['draft_pick'] = "Undrafted"
                elif match_draft:
                    qualified_elements['draft'] = ele
                    year_draft, round, lll, pick = qualified_elements['draft'].replace(',', '').split()
                    # year_draft, round, pick = match_draft.groups()
                    qualified_elements['draft_year'] = year_draft
                    qualified_elements['draft_round'] = round[1:]
                    qualified_elements['draft_pick'] = pick
            else:
                qualified_elements['draft_year'] = "N/A"
                qualified_elements['draft_round'] = "N/A"
                qualified_elements['draft_pick'] = "N/A"

            # find the draft (year only)
            pattern_draft2 = r"^(\d{4})$" # 1996
            if ele and ele.strip():
                match_draft2 = re.match(pattern_draft2, ele)
                if match_draft2:
                    qualified_elements['draft_year'] = ele
                    qualified_elements['draft_round'] = "N/A"
                    qualified_elements['draft_pick'] = "N/A"
            else:
                qualified_elements['draft_year'] = "N/A"
                qualified_elements['draft_round'] = "N/A"
                qualified_elements['draft_pick'] = "N/A"

            # find the height
            pattern_height = r"\d+'(?:\d+(?:\.\d+)?\")?\s\((?:\d+(?:\.\d+)?)m\)"
            imperial_pattern = r"(\d+)'(\d+(?:\.\d+)?)\""
            metric_pattern = r"\((\d+(?:\.\d+)?)m\)"

            if ele and re.match(pattern_height, ele):
                imperial_match = re.search(imperial_pattern, ele)
                metric_match = re.search(metric_pattern, ele)
                if imperial_match:
                    feet, inches = imperial_match.groups()
                    if feet and inches:
                        qualified_elements['height_feet'] = f"{feet}'{inches}\""

                if metric_match:
                    meters = metric_match.group(1)
                    if meters:
                        qualified_elements['height_m'] = f"{meters}"

            # find the weight
            pattern_weight = r"\d+(?:\.\d+)?lb\s\(\d+(?:\.\d+)?kg\)"
            imperial_pattern = r"(\d+(?:\.\d+)?)lb"
            metric_pattern = r"\((\d+(?:\.\d+)?)kg\)"

            if ele and re.match(pattern_weight, ele):
                imperial_match = re.search(imperial_pattern, ele)
                metric_match = re.search(metric_pattern, ele)
                if imperial_match:
                        pounds = imperial_match.group(1)
                        if pounds:
                            qualified_elements['weight_pounds'] = f"{pounds}lb"

                if metric_match:
                        kilograms = metric_match.group(1)
                        if kilograms:
                            qualified_elements['weight_kg'] = f"{kilograms}kg"

        print(qualified_elements)

        dictionary = player_info(
            player=first_name + " " + last_name,
            country=qualified_elements['country'],
            birth=qualified_elements['birth'],
            height_feet=qualified_elements['height_feet'],
            height_m=qualified_elements['height_m'],
            weight_pounds=qualified_elements['weight_pounds'],
            weight_kg=qualified_elements['weight_kg'],
            draft_year=qualified_elements['draft_year'],
            draft_round=qualified_elements['draft_round'],
            draft_pick=qualified_elements['draft_pick']
        )
        yield dictionary