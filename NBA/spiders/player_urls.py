import json
import scrapy
from bs4 import BeautifulSoup
from NBA.items import player_urls_lst
import re
from scrapy_playwright.page import PageMethod


class NbaScraping(scrapy.Spider):
    name = "url"

    @classmethod
    def update_settings(cls, settings) -> None:
        super().update_settings(settings)
        settings.set("PLAYWRIGHT_BROWSER_TYPE", "chromium")
        settings.set("PLAYWRIGHT_LAUNCH_OPTIONS", {"headless": False})
        settings.set("PLAYWRIGHT_MAX_PAGES_PER_CONTEXT", 1)
        settings.set("PLAYWRIGHT_MAX_CONTEXTS", 1)

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.nba.com/players",
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

        # Click the "I Decline" button if it exists
        btn = await page.query_selector("#onetrust-reject-all-handler")
        if btn:
            await btn.click(button="left")

        # Wait for the toggle to be visible
        await page.wait_for_selector("label.Toggle_toggle__2_SBA.PlayerList_toggle__RL_YD")

        # Click the toggle
        toggle = await page.query_selector("label.Toggle_toggle__2_SBA.PlayerList_toggle__RL_YD")
        await toggle.click(button="left")

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

        # Wait for the table rows to be visible
        await page.wait_for_selector("tbody tr")

        soup = BeautifulSoup(await page.content(), "html.parser")

        await page.close()

        # players' info
        player_urls = soup.select(".RosterRow_primaryCol__1lto4")
        for url in player_urls:
            player_url = url.find("a", class_="RosterRow_playerLink__qw1vG").get("href")

            dictionary = player_urls_lst(
                player_url=player_url
            )
            yield dictionary