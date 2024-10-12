import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import nba_scraping
import re
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright

class NbaScraping(scrapy.Spider):
    name = "nba"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium") # or "firefox" or "webkit"
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})

    def start_requests(self):
        start_urls = []
        for page in range(1, 4):
            start_urls.append(
                f"https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season={1995+page}-{str(96+page).zfill(2)}"
            )
        start_urls.append(
            "https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season=1999-00"
        )
        for page in range(1, 25):
            start_urls.append(
                f"https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season={1999+page}-{str(page).zfill(2)}"
            )

        for url in start_urls:
            yield scrapy.Request(
            url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse,
                errback=self.errback_close_page,
        )

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(self, response):
        page = response.meta["playwright_page"]

        # Wait for the dropdowns to be available
        await page.wait_for_selector("select.DropDown_select__4pIg9")

        # Find all dropdowns with the class DropDown_select__4pIg9
        dropdowns = await page.query_selector_all("select.DropDown_select__4pIg9")

        # Iterate through the dropdowns to find the one with the -1 option
        for dropdown in dropdowns:
            options = await dropdown.query_selector_all("option")
            for option in options:
                if await option.get_attribute("value") == "-1":
                    await dropdown.select_option(value="-1")
                    break

        # Wait for the table to be available
        # await page.wait_for_selector("Crom_table__p1iZz")

        soup = BeautifulSoup(await page.content(), "html.parser")

        await page.close()

        # players' name
        player_lst = []
        players = soup.find_all(
            "a", class_=["Anchor_anchor__cSc3P", "Crom_stickySecondColumn__29Dwf"]
        )
        for player in players:
            href = player.get("href", "")
            match = re.search(r"stats/player/(\d+)", href)
            if match:
                player_name = player.get_text()
                player_lst.append(player_name)

        # teams' name
        team_lst = []
        teams = soup.find_all("a", class_=["Crom_text__NpR1_", "Anchor_anchor__cSc3P"])
        for team in teams:
            href = team.get("href", "")
            match = re.search(r"stats/team/(\d+)", href)
            if match:
                team_name = team.get_text()
                team_lst.append(team_name)

        # stats
        stats_lst = []
        tbody = soup.find("tbody", class_="Crom_body__UYOcU")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                stats = row.find_all("td")
                row_stats = []
                for stat in stats:
                    player_stat = stat.get_text()
                    row_stats.append(player_stat)
                stats_lst.append(row_stats)

        for i in range(len(stats_lst)):
            stats_lst[i] = (stats_lst[i])[3:]

        player_team_mapping = zip(player_lst, team_lst, stats_lst)

        for player, team, stat in player_team_mapping:
            dictionary = nba_scraping(
                player=player,
                team=team,
                age=stat[0],
                gp=stat[1],
                wins=stat[2],
                losses=stat[3],
                min=stat[4],
                pts=stat[5],
                fgm=stat[6],
                fga=stat[7],
                fg_pct=stat[8],
                three_pm=stat[9],
                three_pa=stat[10],
                three_ppct=stat[11],
                ftm=stat[12],
                fta=stat[13],
                ft_pct=stat[14],
                oreb=stat[15],
                dreb=stat[16],
                reb=stat[17],
                ast=stat[18],
                tov=stat[19],
                stl=stat[20],
                blk=stat[21],
                pf=stat[22],
                fp=stat[23],
                dd2=stat[24],
                td3=stat[25],
                plus_minus_box=stat[26],
            )
            yield dictionary
