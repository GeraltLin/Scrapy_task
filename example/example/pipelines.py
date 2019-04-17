# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from pymysql import *


class ExamplePipeline(object):
    def process_item(self, item, spider):
        return item


class PriceConverterPipeline(object):
    # 汇率转换
    def __init__(self):
        self.exchange_rate = 8.5309

    def process_item(self, item, spider):
        price = float(item['price'][1:]) * self.exchange_rate
        item['price'] = '￥%.2f' % price
        return item


class DuplicatesPipeline(object):
    # 去除重复
    def __init__(self):
        self.bool_set = set()

    def process_item(self, item, spider):
        name = item['name']
        if name in self.bool_set:
            raise DropItem("Duplicate book found:{}".format(name))
        self.bool_set.add(name)
        return item


class MysqlPipeline(object):
    # 去除重复
    def __init__(self):
        self.DB_URI = 'localhost'
        self.DB_NAME = 'books_test'

    def open_spider(self,spider):
        self.conn = connect(host=self.DB_URI, port=3306, database=self.DB_NAME, user='root', password='lwxqq220114',
                            charset='utf8')
        self.cs = self.conn.cursor()

    def close_spider(self,spider):
        self.cs.close()
        self.conn.close()

    def process_item(self, item, spider):
        bookname = item['name']
        bookprice = item['price']
        self.cs.execute("insert into books(name,price) values(%s, %s)",(bookname,bookprice))
        self.conn.commit()
        return item
