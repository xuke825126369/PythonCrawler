# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from .spiders.zlzp import ZlzpSpider
from .spiders.wyjob import WyjobSpider
from .spiders.zbtong import ZbtongSpider
from .spiders.neitui import NeituiSpider

from .items import SpecItem,NewsItem,ZpItem

class TutorialsPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    collection_name = 'scrapy_ershoufang_items'
    collection_name1 = 'scrapy_cj_ershoufang_items'
    zp_collection_name = 'zp_info_table'
    oly_collection_name = 'aoyun_news_table'
    oly_spec_collection = 'aoyun_spec_table'

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE','items')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        if isinstance(item,SpecItem):
            self.db[self.oly_spec_collection].insert(dict(item))
        elif isinstance(item,NewsItem):
            key_index = item['url']
            if not self.db[self.oly_collection_name].find({'url':key_index}).count():
                self.db[self.oly_collection_name].insert(dict(item))
        else:
            key_index = item['url']
            if not self.db[self.zp_collection_name].find({'url':key_index}).count():
                self.db[self.zp_collection_name].insert(dict(item))
        return item