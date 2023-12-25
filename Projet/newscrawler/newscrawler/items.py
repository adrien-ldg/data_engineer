# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    player = scrapy.Field()
    month_born = scrapy.Field()
    year_born = scrapy.Field()
    age = scrapy.Field()
    nationality = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    team = scrapy.Field()
    MJ = scrapy.Field()
    minutes = scrapy.Field()
    tir = scrapy.Field()
    tir_3_pts = scrapy.Field()
    lf = scrapy.Field()
    rb_off = scrapy.Field()
    rb_df = scrapy.Field()
    rb = scrapy.Field()
    pd = scrapy.Field()
    bp = scrapy.Field()
    inter = scrapy.Field()
    ct = scrapy.Field()
    fte = scrapy.Field()
    pts = scrapy.Field()
    
    
