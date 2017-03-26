# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InterwettenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kaisaishijian = scrapy.Field()
    zhudui = scrapy.Field()
    kedui = scrapy.Field()
    zhupei = scrapy.Field()
    pingpei = scrapy.Field()
    kepei = scrapy.Field()
    suoshuliansai = scrapy.Field()
    zhuaqushijian = scrapy.Field()
    laiyuanzhandian = scrapy.Field()
