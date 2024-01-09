# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import re


class TextPipeline(object):
    
    def process_item(self, item, spider):
        if item["player"] and item["team"]:
            item["player"] = clean_spaces(item["player"])
            item["team"] = clean_spaces(item["team"])
            item["month_born"] = re.split(r"[()]", item["month_born"])
            item["month_born"] = item["month_born"][0].split()[1].strip()
            item["year_born"] = re.split(r"[()]", item["year_born"])
            item["year_born"] = item["year_born"][0].split()[2].strip()
            item["age"] = re.split(r"[()]", item["age"])
            item["age"] = re.sub(r'\D', '', item["age"][1])
            item["nationality"] = item["nationality"].split("/")
            item["size"] = re.sub(r'\D', '', item["size"])
            item["weight"] = re.sub(r'\D', '', item["weight"])
            item["pick_draft"] = item["pick_draft"].split(",")
            try:
                item["pick_draft"] = item["pick_draft"][1]
                item["pick_draft"] = re.sub(r'\D', '', item["pick_draft"])
            except:
                item["pick_draft"] = "non drafte"
                
            return item
        else:
            raise DropItem("Missing value in %s" % item)


def clean_spaces(string):
    if string:
        return " ".join(string.split())
    

class NumericPipeline(object):

    def process_item(self, item, spider):
        for i in ["minutes", "tir", "tir_3_pts", "lf", "rb_off", "rb_df", "rb", "pd", "bp", "inter", "ct", "fte", "pts"]:
            try:
                item[i] = float(item[i])
            except ValueError:
                item[i] = 0.0

        for i in ["MJ", "year_born", "age", "size", "weight"]:
            try:
                item[i] = int(item[i])
            except ValueError:
                item[i] = 0
                
        try:
            item["pick_draft"] = int(item["pick_draft"])
        except ValueError:
            item["pick_draft"] = "non drafte"
                
        return item
    
    
class MongoPipeline(object):

    collection_name = 'nba_player'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["basket"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update_one({"player": dict(item)["player"]}, {"$set": dict(item)}, upsert=True)
        return item
