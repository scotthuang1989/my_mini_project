# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy import signals
from scrapy.exceptions import DropItem
import hashlib


class BaidunewsDBPipeline(object):
  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    self.db = sqlite3.connect('baidunews.db')
    self.db_cursor = self.db.cursor()

  def spider_closed(self, spider):
    self.db.commit()
    self.db.close()

  def process_item(self, item, spider):
    hash = hashlib.sha256()
    hash.update(item['news_title'].encode())
    title_hash = hash.digest()
    self.db_cursor.execute("SELECT * from finance_news WHERE id=?", (title_hash,))
    if not self.db_cursor.fetchall():
      self.db_cursor.execute('INSERT INTO finance_news (id, title, url) VALUES (?, ?, ?)',\
                             (title_hash, item['news_title'], item['news_url']))
    raise DropItem("item have been saved to db")
