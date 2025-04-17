import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import game_results
from scrapy.crawler import CrawlerProcess
import re
from datetime import datetime
from scrapy_playwright.page import PageMethod

class GameResults(scrapy.Spider):
    name = "gameresults"

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
            url = f"https://www.nba.com/stats/teams/boxscores?Season={start_year}-{end_year:02d}&SeasonType=Regular+Season"
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
                        dictionary = game_results(
                            team_team=stat[0],
                            matchup_team=stat[1][-2:],
                            gamedate_team=stat[2],
                            w_l_team=stat[3],
                            min_team=float(stat[4]),
                            pts_team=float(stat[5]),
                            fgm_team=float(stat[6]),
                            fga_team=float(stat[7]),
                            fg_pct_team=float(stat[8]),
                            three_pm_team=float(stat[9]),
                            three_pa_team=float(stat[10]),
                            three_pct_team=float(stat[11]),
                            ftm_team=float(stat[12]),
                            fta_team=float(stat[13]),
                            ft_pct_team=float(stat[14]),
                            oreb_team=float(stat[15]),
                            dreb_team=float(stat[16]),
                            reb_team=float(stat[17]),
                            ast_team=float(stat[18]),
                            stl_team=float(stat[19]),
                            blk_team=float(stat[20]),
                            tov_team=float(stat[21]),
                            pf_team=float(stat[22]),
                            plus_minus_box_team=float(stat[23])
                        )
                        yield dictionary

        await page.close()

# Note: To interacte effectively with button(s),
# Perform the actions first to all of them, then wait for the page to load at the end