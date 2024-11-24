# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# import json
# from dataclasses import asdict
# from NBA.items import nba_scraping


# class NbaPipeline:
#     def open_spider(self, spider):
#         self.file = open("nba_players.jsonl", "w")

#     def close_spider(self, spider):
#         self.file.close()

#     def process_item(self, item: nba_scraping, spider):
#         dictionary = asdict(item)
#         json.dump(dictionary, self.file)
#         self.file.write("\n")
        
#         return item