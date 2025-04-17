import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import nba_scraping
import re
from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright

class SeasonalStats(scrapy.Spider):
    name = "nba"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("CONCURRENT_REQUESTS", 1)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium") # or "firefox" or "webkit"
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("DOWNLOAD_DELAY", 16)

    def start_requests(self):
        start_urls = []
        for page in range(1, 4):
            start_urls.append(
                f"https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season={1995+page}-{str(96+page).zfill(2)}"
            )
        start_urls.append(
            "https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season&Season=1999-00"
        )
        for page in range(1, 26):
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

        year_match = re.search(r"Season=(\d{4})-\d{2}", response.url)
        if year_match:
            year = int(year_match.group(1))
        else:
            if "1900-00" in response.url:
                year = 1999
            else:
                year = None
                self.logger.warning(f"Could not extract the year from the URL: {response.url}")

        # Wait for the dropdowns to be available
        await page.wait_for_selector("select.DropDown_select__4pIg9", timeout=5000)

        # Find all dropdowns with the class DropDown_select__4pIg9
        dropdowns = await page.query_selector_all("select.DropDown_select__4pIg9")

        # Iterate through the dropdowns to find the one with the -1 option
        for dropdown in dropdowns:
            options = await dropdown.query_selector_all("option")
            for option in options:
                if await option.get_attribute("value") == "-1":
                    await dropdown.select_option(value="-1")
                    await page.wait_for_timeout(2000)
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
                team_playerseason=team,
                year_playerseason=year,
                age_playerseason=stat[0],
                gp_playerseason=int(stat[1]),
                wins_playerseason=int(stat[2]),
                losses_playerseason=int(stat[3]),
                min_playerseason=float(stat[4]),
                pts_playerseason=float(stat[5]),
                fgm_playerseason=float(stat[6]),
                fga_playerseason=float(stat[7]),
                fg_pct_playerseason=float(stat[8]),
                three_pm_playerseason=float(stat[9]),
                three_pa_playerseason=float(stat[10]),
                three_ppct_playerseason=float(stat[11]),
                ftm_playerseason=float(stat[12]),
                fta_playerseason=float(stat[13]),
                ft_pct_playerseason=float(stat[14]),
                oreb_playerseason=float(stat[15]),
                dreb_playerseason=float(stat[16]),
                reb_playerseason=float(stat[17]),
                ast_playerseason=float(stat[18]),
                tov_playerseason=float(stat[19]),
                stl_playerseason=float(stat[20]),
                blk_playerseason=float(stat[21]),
                pf_playerseason=float(stat[22]),
                fp_playerseason=float(stat[23]),
                dd2_playerseason=float(stat[24]),
                td3_playerseason=float(stat[25]),
                plus_minus_box_playerseason=float(stat[26]),
            )
            yield dictionary
