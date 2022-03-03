# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name = "renta_cdmx"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://andatti2:andatti2@cluster0.lcbrk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client["lamudi_cdmx"]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

#class LamudiPipeline:
#    def process_item(self, item, spider):
#        return item
