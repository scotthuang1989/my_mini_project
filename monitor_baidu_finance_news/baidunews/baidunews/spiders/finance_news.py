# -*- coding: utf-8 -*-
import scrapy
from baidunews.items import BaiduFinancenewsItem


class FinanceNewsSpider(scrapy.Spider):
    name = 'finance_news'
    allowed_domains = ['baidu.com']
    start_urls = ['http://news.baidu.com/finance']


    def parse(self, response):
        fb_ulist = response.xpath("//ul[@class='ulist fb-list']")
        for ul in fb_ulist:
          news_href_list = ul.xpath("./li/a/@href").extract()
          news_title_list = ul.xpath("./li/a/text()").extract()
          for item in list(zip(news_href_list,news_title_list)):
            yield BaiduFinancenewsItem(name="Fnews", news_title=item[1],
                                       news_url=item[0])
