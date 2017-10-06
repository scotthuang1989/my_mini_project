
# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
import jdBookScrapy
import os

class JdbookscrapyPipeline(object):
    def open_spider(self, spider):
        self.csv_fd=open(os.path.join(jdBookScrapy.DATA_PATH ,"jdbookexporter.csv"),'wb')
        # import pdb; pdb.set_trace()
        self.csv_exporter = CsvItemExporter(file=self.csv_fd)
        self.csv_exporter.start_exporting()

    def close_spider(self, spider):
        self.csv_exporter.finish_exporting()
        self.csv_fd.close()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        raise DropItem("item is processed")
