import json
import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
from NBA.items import nba_scraping


class NbaScraping(scrapy.Spider):
    name = 'nba'

    def start_requests(self):
        yield scrapy.Request(
            "https://www.nba.com/stats/players/traditional",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_coroutines=[
                    PageMethod('wait_for_selector',
                               'div#Block_blockContent__6iJ_n')
                ]
            )
        ) 

    async def parse(self, response):
        for player in response.css('div.Crom_container__C45Ti crom-container'):
            yield {
                'player': player.css('a', class_="Anchor_anchor__cSc3P").get_text()
            }

        # dictionary = nba_scraping(      
        #     player=players