# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HuxiuPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.253.128',user='root', password='mysql', database='mine', )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item.get('title')
        url = item.get('url')
        name = item.get('name')
        write_time = item.get('write_time')
        comment = item.get('comment')
        favorites = item.get('favorites')
        abstract = item.get('abstract')
        insert_sql = "insert into huxiu_db(title,url,name,write_time, comment, favorites, abstract)VALUES (%s, %s, %s, %s,%s,%s,%s);"
        self.cursor.execute(insert_sql, (title,url,name,write_time, comment, favorites, abstract))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
