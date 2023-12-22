# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    
    def process_item(self, item, spider):
        if item["player"] and item["team"]:
            item["player"] = clean_spaces(item["player"])
            item["team"] = clean_spaces(item["team"])
            for i in ["MJ", "minutes", "tir", "tir_3_pts", "lf", "rb_off", "rb_df", "rb", "pd", "bp", "inter", "ct", "fte", "pts"]:
                if not item[i]:
                    item[i] = 0.0
                try:
                    item[i] = float(item[i])
                except ValueError:
                    item[i] = 0.0
            return item
        else:
            raise DropItem("Missing value in %s" % item)


def clean_spaces(string):
    if string:
        return " ".join(string.split())
    
    
class MongoPipeline(object):

    collection_name = 'nba_player'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["basket"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
