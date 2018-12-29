# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import json
import pymysql

class ItjuziPipeline(object):
    def process_item(self, item, spider):
        item['data_source'] = spider.name
        item['data_time'] = datetime.utcnow()
        return item


class juziPipeline(object):
    def open_spider(self, spider):
        self.file = open('juzinvst.json', 'w')

    def process_item(self, item, spider):
        str_data = json.dumps(dict(item), ensure_ascii=False)+','
        self.file.write(str_data)
        return item

    def close_spider(self, spider):
        self.file.close()


class JuziToDBPipeline(object):

    def open_spider(self, spider):
        self.db = pymysql.connect("localhost", "root", "mysql", 'mine')

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO itjuzi VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)


class InvstToDBPipeline(object):

    def open_spider(self, spider):
        self.db = pymysql.connect("localhost", "root", "mysql", 'mine')

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO JuZIinvst VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)


class PersonToDBPipeline(object):

    def open_spider(self, spider):
        self.db = pymysql.connect("localhost", "root", "mysql", 'mine')

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        self.db.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO JuZIperson VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)