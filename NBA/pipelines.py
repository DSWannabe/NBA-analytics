# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from dataclasses import asdict
from NBA.items import nba_scraping, game_stats, player_urls_lst, player_info
import os
from scrapy.exceptions import NotConfigured


class NbaPipeline:
    def __init__(self, output_folder: str, file_name: str):
        self.output_folder = output_folder
        self.file_name = file_name

    @classmethod
    def from_crawler(cls, crawler):
        output_folder = crawler.settings.get("NBA_PIPELINE_OUTPUT_FOLDER")
        if not output_folder:
            raise NotConfigured("NBA_PIPELINE_OUTPUT_FOLDER is not set")
        file_name = cls.file_name
        return cls(output_folder, file_name)

    def open_spider(self, spider):
        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

        # Construct the output file path
        file_path = os.path.join(self.output_folder, self.file_name)
        self.file = open(file_path, "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, self.item_class):
            dictionary = asdict(item)
            json.dump(dictionary, self.file)
            self.file.write("\n")
        return item

class GameStatsPipeline(NbaPipeline):
    file_name = "nba_players_game_stats.jsonl"
    item_class = game_stats

class SeasonalStatsPipeline(NbaPipeline):
    file_name = "nba_players_seasonal_stats.jsonl"
    item_class = nba_scraping

class PlayerUrlsPipeline(NbaPipeline):
    file_name = "player_urls.jsonl"
    item_class = player_urls_lst

class PlayerInfoPipeline(NbaPipeline):
    file_name = "player_info.jsonl"
    item_class = player_info
