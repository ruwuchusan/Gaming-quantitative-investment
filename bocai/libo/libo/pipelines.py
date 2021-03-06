# -*- coding: utf-8 -*-
from libo.items import LiboItem
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LiboPipeline(object):

    def __init__(self):
        pass


    def open_spider(self, spider):
        self.client = pymongo.MongoClient('192.168.1.10:8822')
        self.collection = self.client['db']['ladbrokes']
        self.collection.remove({})
        self.collection_1 = self.client['db_bak']['ladbrokes']



    def save(self,item):
        self.collection.insert(dict(item))
        self.collection_1.insert(dict(item))


    def process_item(self,item,spider):
        if isinstance(item,LiboItem):
            self.save(item)
        return item


    def close_spider(self, spider):
        self.client.close()
