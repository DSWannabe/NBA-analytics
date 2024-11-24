import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import game_stats
from scrapy.crawler import CrawlerProcess
import re
from datetime import datetime

class GameStats(scrapy.Spider):
    name = "game"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium") # or "firefox" or "webkit"
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("CONCURRENT_REQUESTS", 1)
        settings.set("DOWNLOAD_DELAY", 8)


    def start_requests(self):
        start_urls = []
        for page in range(1, 4):
            start_urls.append(
                f"https://www.nba.com/stats/players/boxscores?Season={1995+page}-{str(96+page).zfill(2)}&SeasonType=Regular+Season"
            )

        start_urls.append(
            "https://www.nba.com/stats/players/boxscores?Season=1999-00&SeasonType=Regular+Season"
        )
        for page in range(1, 25):
            start_urls.append(
                f"https://www.nba.com/stats/players/boxscores?Season={1999+page}-{str(page).zfill(2)}&SeasonType=Regular+Season"
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

        stats_lst = []
        tbody = soup.find("tbody", class_="Crom_body__UYOcU")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                stats = row.find_all("td")
                row_stats = []
                for stat in stats:
                        player_stat = stat.get_text()
                        if player_stat == "-":
                            row_stats.append(0)
                        else:
                            row_stats.append(player_stat)
                stats_lst.append(row_stats)

        for stat in stats_lst:
            dictionary = game_stats(
                player=stat[0],
                team=stat[1],
                against=stat[2][-3:],
                gamedate=stat[3],
                w_l=stat[4],
                min=float(stat[5]),
                pts=float(stat[6]),
                fgm=float(stat[7]),
                fga=float(stat[8]),
                fg_pct=float(stat[9]),
                three_pm=float(stat[10]),
                three_pa=float(stat[11]),
                three_ppct=float(stat[12]),
                ftm=float(stat[13]),
                fta=float(stat[14]),
                ft_pct=float(stat[15]),
                oreb=float(stat[16]),
                dreb=float(stat[17]),
                reb=float(stat[18]),
                ast=float(stat[19]),
                stl=float(stat[20]),
                blk=float(stat[21]),
                tov=float(stat[22]),
                pf=float(stat[23]),
                plus_minus_box=float(stat[24]),
                fp=float(stat[25]),
            )
            yield dictionary

# Note: To interacte effectively with button(s),
# Perform the actions first to all of them, then wait for the page to load at the end