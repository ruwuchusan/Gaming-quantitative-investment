# -*- coding: utf-8 -*-
import pymongo
from weilian.items import WeilianItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeilianPipeline(object):
    def __init__(self):
        pass


    def open_spider(self, spider):
        self.client = pymongo.MongoClient('192.168.1.10:8822')
        self.collection = self.client['db']['weilianxier']
        self.collection.remove({})
        self.collection_1 = self.client['db_bak']['weilianxier']


    def save(self,item):
        self.collection.insert(dict(item))
        self.collection_1.insert(dict(item))


    def process_item(self,item,spider):
        if isinstance(item,WeilianItem):
            self.save(item)
        return item


    def close_spider(self, spider):
        self.client.close()