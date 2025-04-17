import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import player_info2
from scrapy.crawler import CrawlerProcess
import re
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright
from NBA.const import COUNTRIES, MONTH_MAP
from datetime import datetime

class PlayerInfo(scrapy.Spider):
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
        settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", 16)
        settings.set("AUTOTHROTTLE_START_DELAY", 0.1)
        settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

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
        soup = BeautifulSoup(response.text, "html.parser")

        # players' id
        player_id_match = re.search(r"/player/(\d+)", response.url)
        player_id = player_id_match.group(1) if player_id_match else "Unknown"

        # players' name
        name_elements = response.css('div.PlayerSummary_mainInnerBio__JQkoj h1.PlayerSummary_playerNameText___MhqC::text').getall()
        name = name_elements[0] if len(name_elements[0]) > 1 else "NA"

        # other player information
        elements = soup.find('div', class_='PlayerSummary_hw__HNuGb')

        qualified_elements = {}

        for ele in elements:
            columns = ele.find_all_next('div', class_='PlayerSummary_playerInfo__om2G4')
            for col in columns:
                value = col.find_next('p', class_='PlayerSummary_playerInfoValue__JS8_v').get_text()
                key = col.find_next('p', class_='PlayerSummary_playerInfoLabel__hb5fs').get_text()
                qualified_elements[key] = value

        # process height
        pattern_height = r"\d+'(?:\d+(?:\.\d+)?\")?\s\((?:\d+(?:\.\d+)?)m\)"
        imperial_pattern = r"(\d+)'(\d+(?:\.\d+)?)\""
        metric_pattern = r"\((\d+(?:\.\d+)?)m\)"
        if qualified_elements['HEIGHT'] == "--":
            qualified_elements['height_m'] = 0
            qualified_elements['height_ft'] = 0
        elif qualified_elements['HEIGHT'] and re.match(pattern_height, qualified_elements['HEIGHT']):
            imperial_match = re.match(imperial_pattern, qualified_elements['HEIGHT'])
            metric_match = re.search(metric_pattern, qualified_elements['HEIGHT'])
            if imperial_match:
                feet, inches = imperial_match.groups()
                qualified_elements['height_ft'] = f"{feet}'{inches}\""
            if metric_match:
                height_in_m = round(float(metric_match.group(1)) * 100, 1)
                qualified_elements['height_m'] = height_in_m

        # process weight
        pattern_weight = r"\d+(?:\.\d+)?lb\s\(\d+(?:\.\d+)?kg\)"
        imperial_pattern = r"(\d+(?:\.\d+)?)lb"
        metric_pattern = r"\((\d+(?:\.\d+)?)kg\)"

        if qualified_elements['WEIGHT'] == "--":
            qualified_elements['weight_pounds'] = 0
            qualified_elements['weight_kg'] = 0
        elif qualified_elements['WEIGHT'] and re.match(pattern_weight, qualified_elements["WEIGHT"]):
            imperial_match = re.search(imperial_pattern, qualified_elements['WEIGHT'])
            metric_match = re.search(metric_pattern, qualified_elements['WEIGHT'])
            if imperial_match:
                pounds = imperial_match.group(1)
                qualified_elements['weight_pounds'] = float(pounds)
            if metric_match:
                kilograms = metric_match.group(1)
                qualified_elements['weight_kg'] = float(kilograms)

        # process draft
        pattern_draft = r"(\d{4})\sR(\d+)\sPick\s(\d+)"
        pattern_year_draft = r"(\d{4})"
        if qualified_elements['DRAFT'] == 'Undrafted':
            qualified_elements['draft_year'] = 'Undrafted'
            qualified_elements['draft_round'] = 'Undrafted'
            qualified_elements['draft_pick'] = 'Undrafted'
        elif qualified_elements['DRAFT'] == '--':
            qualified_elements['draft_year'] = 'N/A'
            qualified_elements['draft_round'] = 'N/A'
            qualified_elements['draft_pick'] = 'N/A'
        elif qualified_elements['DRAFT'] and re.match(pattern_draft, qualified_elements['DRAFT']):
            year_draft, round_draft, lll, pick = qualified_elements['DRAFT'].replace(',', '').split()
            qualified_elements['draft_year'] = year_draft
            qualified_elements['draft_round'] = round_draft[1:]
            qualified_elements['draft_pick'] = pick
        elif qualified_elements['DRAFT'] and re.match(pattern_year_draft, qualified_elements['DRAFT']):
            qualified_elements['draft_year'] = qualified_elements['DRAFT']
            qualified_elements['draft_round'] = 'N/A'
            qualified_elements['draft_pick'] = 'N/A'

        dictionary = player_info2(
            player_id=player_id,
            player=name,
            height_m=qualified_elements['height_m'],
            height_ft=qualified_elements['height_ft'],
            weight_pounds=qualified_elements['weight_pounds'],
            weight_kg=qualified_elements['weight_kg'],
            country=qualified_elements['COUNTRY'],
            birth=qualified_elements['BIRTHDATE'],
            draft_year=qualified_elements['draft_year'],
            draft_round=qualified_elements['draft_round'],
            draft_pick=qualified_elements['draft_pick']
        )

        yield dictionary

    def logresult(self, result):
        cnt = 0
        with open("data/player_info2.jsonl", "a") as file:
            for line in file:
                cnt += 1
        self.log(f"total row: {cnt}")