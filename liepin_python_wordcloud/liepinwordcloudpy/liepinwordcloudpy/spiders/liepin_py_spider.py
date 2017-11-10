# -*- coding: utf-8 -*-
import scrapy
from decouple import config
from scrapy.http import Request
import logging
import functools

from liepinwordcloudpy import items


class LiepinPySpiderSpider(scrapy.Spider):
    name = 'liepin_py_spider'
    allowed_domains = ['www.liepin.com']
    start_url_template = config('START_URL_TEMP')

    def start_requests(self):
        for i in range(100):
            yield Request(self.start_url_template.format(i))

    def parse(self, response):
        """
        this function will process the page which contains list of job.
        The responsibility of this page is to extract jobinfo url and yield request
        """
        joblist = response.xpath("//ul[@class='sojob-list']/li")
        for job in joblist:
            joburl=job.xpath("./div/div/h3/a/@href").extract()[0]
            yield Request(url=joburl, callback=self.parse_job_info)


    def parse_job_info(self, response):
        """
        this function process the page of particular job.
        it will extract job description and requirement.
        """
        job_content = response.xpath(
                    "//div[@class='content content-word']/text()").extract()
        content = functools.reduce(lambda x,y:x+y, job_content)
        content = content.strip()
        return items.LiepinwordcloudpyItem(job_content=content, job_url=response.url)
