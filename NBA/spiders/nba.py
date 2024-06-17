import json
import scrapy
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
        
        self.log(response.text, response.status)
        # players' name
        player_name = soup.find_all("a", class_="Anchor_anchor__cSc3P")
        filered_player = [
            play for play in player_name if '/stats/player/' in play['href']
            ]
        players = [name.text for name in filered_player]     
        dictionary = nba_scraping(
            player=players
        )
        yield dictionary
