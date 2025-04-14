import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import player_game_stats
from scrapy.crawler import CrawlerProcess
import re
from datetime import datetime
from scrapy_playwright.page import PageMethod

class GameStats(scrapy.Spider):
    name = "playergamestats"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium") # or "firefox" or "webkit"
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("CONCURRENT_REQUESTS", 1)
        settings.set("DOWNLOAD_DELAY", 16)


    def start_requests(self):
        start_urls = []
        for page in range(1, 2):
            start_year = 2016 + page
            end_year = (17 + page) % 100
            url = f"https://www.nba.com/stats/players/boxscores?Season={start_year}-{end_year:02d}&SeasonType=Regular+Season"
            start_urls.append(url)

        for url in start_urls:
            yield scrapy.Request(
            url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle", timeout=60000)
                        ],
                    },
                callback=self.parse,
                errback=self.errback_close_page,
        )

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(60000)

        # Wait for the dropdowns to be available
        await page.wait_for_selector("select.DropDown_select__4pIg9", timeout=60000, state="visible")

        # Find all dropdowns with the class DropDown_select__4pIg9
        dropdowns = await page.query_selector_all("select.DropDown_select__4pIg9")

        # Iterate through the dropdowns to find the one with the -1 option
        for dropdown in dropdowns:
            options = await dropdown.query_selector_all("option")
            for option in options:
                option_value = await option.get_attribute("value")
                if option_value != "-1" and option_value.isdigit():
                    await dropdown.select_option(value=option_value)

                    await page.wait_for_timeout(2000)

                    # Wait for the table to be available
                    # await page.wait_for_selector("Crom_table__p1iZz", timeout=10000)

                    soup = BeautifulSoup(await page.content(), "html.parser")

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
                        dictionary = player_game_stats(
                            player=stat[0],
                            team_playergame=stat[1],
                            against_playergame=stat[2][-3:],
                            gamedate_playergame=stat[3],
                            w_l_playergame=stat[4],
                            min_playergame=float(stat[5]),
                            pts_playergame=float(stat[6]),
                            fgm_playergame=float(stat[7]),
                            fga_playergame=float(stat[8]),
                            fg_pct_playergame=float(stat[9]),
                            three_pm_playergame=float(stat[10]),
                            three_pa_playergame=float(stat[11]),
                            three_ppct_playergame=float(stat[12]),
                            ftm_playergame=float(stat[13]),
                            fta_playergame=float(stat[14]),
                            ft_pct_playergame=float(stat[15]),
                            oreb_playergame=float(stat[16]),
                            dreb_playergame=float(stat[17]),
                            reb_playergame=float(stat[18]),
                            ast_playergame=float(stat[19]),
                            stl_playergame=float(stat[20]),
                            blk_playergame=float(stat[21]),
                            tov_playergame=float(stat[22]),
                            pf_playergame=float(stat[23]),
                            plus_minus_box_playergame=float(stat[24]),
                            fp_playergame=float(stat[25]),
                        )
                        yield dictionary

        await page.close()

# Note: To interacte effectively with button(s),
# Perform the actions first to all of them, then wait for the page to load at the end