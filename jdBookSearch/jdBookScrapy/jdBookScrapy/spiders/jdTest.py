# -*- coding: utf-8 -*-
import scrapy


class JdtestSpider(scrapy.Spider):
    name = 'jdTest'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def parse(self, response):
        pass
