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
            )
        ) 

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        # If you need anything, just select from soup like usual
        # dictionary = nba_scraping(
        #     player=players