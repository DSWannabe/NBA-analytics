import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import player_info
from scrapy.crawler import CrawlerProcess
import re
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright
from NBA.const import COUNTRIES

class NbaScraping(scrapy.Spider):
    name = "info"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium")
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("CONCURRENT_REQUESTS", 16)
        settings.set("DOWNLOAD_DELAY", 0.5)
        settings.set("AUTOTHROTTLE_TARGET_CONCURRENCY", 16)
        settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", 8)

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
            pattern_country = r"\b[A-Za-z]+\b"
            if ele and re.match(pattern_country, ele):
                if ele not in qualified_elements:
                    for country in COUNTRIES:
                        if ele == country['name']:
                            qualified_elements['country'] = country['name']
                            break
                        elif ele == country['code']:
                            qualified_elements['country'] = country['code']
                            break
                        else:
                            qualified_elements['country'] = 'N/A' # Clean later
            else:
                qualified_elements['country'] = 'N/A'

            # find the birth date
            pattern = r"(?i)(January|February|March|April|May|June|July|August|September|October|November|December)\s([1-9]|[12][0-9]|3[01]),\s\d{4}"
            if ele and re.match(pattern, ele):
                if ele not in qualified_elements:
                    qualified_elements['birth'] = ele
            else:
                qualified_elements['birth'] = 'N/A'

            # find the draft
            pattern_draft = r"(\d{4})\sR(\d+)\sPick\s(\d+)"
            if ele and re.match(pattern_draft, ele):
                if ele not in qualified_elements:
                    qualified_elements['draft'] = ele
            else:
                qualified_elements['draft'] = 'undrafted'

            # find the height
            pattern_height = r"\d+'(?:\d+(?:\.\d+)?\")?\s\((?:\d+(?:\.\d+)?)m\)"
            imperial_pattern = r"(\d+)'(\d+(?:\.\d+)?)\""
            metric_pattern = r"\((\d+(?:\.\d+)?)m\)"

            if ele and re.match(pattern_height, ele):
                imperial_match = re.search(imperial_pattern, ele)
                metric_match = re.search(metric_pattern, ele)
                if imperial_match and imperial_match not in qualified_elements:
                    feet, inches = imperial_match.groups()
                    if feet and inches:
                        qualified_elements['height_feet'] = f"{feet}'{inches}\""
                    else:
                        qualified_elements['height_feet'] = 'N/A'
                else:
                    qualified_elements['height_feet'] = 'N/A'

                if metric_match and metric_match not in qualified_elements:
                    meters = metric_match.group(1)
                    if meters:
                        qualified_elements['height_cm'] = f"{meters}m"
                    else:
                        qualified_elements['height_cm'] = 'N/A'
                else:
                    qualified_elements['height_cm'] = 'N/A'
            else:
                qualified_elements['height_cm'] = 'N/A'
                qualified_elements['height_feet'] = 'N/A'

            # find the weight
            pattern_weight = r"\d+(?:\.\d+)?lb\s\(\d+(?:\.\d+)?kg\)"
            imperial_pattern = r"(\d+(?:\.\d+)?)lb"
            metric_pattern = r"\((\d+(?:\.\d+)?)kg\)"

            if ele and re.match(pattern_weight, ele):
                imperial_match = re.search(imperial_pattern, ele)
                if imperial_match and imperial_match not in qualified_elements:
                        pounds = imperial_match.group(1)
                        qualified_elements['weight_pounds'] = f"{pounds}lb"
                else:
                    qualified_elements['weight_pounds'] = 'N/A'

                metric_match = re.search(metric_pattern, ele)
                if metric_match and metric_match not in qualified_elements:
                        kilograms = metric_match.group(1)
                        qualified_elements['weight_kg'] = f"{kilograms}kg"
                else:
                    qualified_elements['weight_kg'] = 'N/A'
            else:
                qualified_elements['weight_kg'] = 'N/A'

        print(qualified_elements)

        dictionary = player_info(
            player=first_name + " " + last_name,
            country=qualified_elements['country'],
            birth=qualified_elements['birth'],
            draft=qualified_elements['draft'],
            height_feet=qualified_elements['height_feet'],
            height_cm=qualified_elements['height_cm'],
            weight_pounds=qualified_elements['weight_pounds'],
            weight_kg=qualified_elements['weight_kg']
        )
        yield dictionary