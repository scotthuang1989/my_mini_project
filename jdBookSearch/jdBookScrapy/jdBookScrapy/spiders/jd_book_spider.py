# -*- coding: utf-8 -*-
import scrapy
import logging
from ..items import JdbookscrapyItem
import os
from urllib.request import urlopen
import jdBookScrapy


IMAGE_PATH=jdBookScrapy.DATA_PATH

class JdBookScrapy(scrapy.Spider):
    name = 'jdBookSpider'
    allowed_domains = ['jd.com','item.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=python&enc=utf-8&wq=python&pvid=6c82d0fcbc5a460dae49eec3a008b460']

    def parse(self, response):
        goods_list = response.xpath("//div[@id='J_goodsList']/ul/li")
        for good in goods_list:
            good_ref=good.xpath("./div/div[@class='p-img']/a/@href").extract()[0]
            if good_ref.startswith("//"):
                good_ref=good_ref[2:]
            if good_ref.startswith("item.jd.com"):
                # logging.error("myurf:"+good_ref)
                yield scrapy.Request(url="http://"+good_ref,
                                    callback=self.parseItem)
            # good_title = good.xpath("./div/div[@class='p-img']/a/@title").extract()
            # good_title = good_title[0].split(' ')[0]
            # good_img_link = good.xpath("./div/div[@class='p-img']/a/img/@src").extract()
            # good_img_link = good_img_link[0][2:]
            # print(good_title, good_img_link)
    def parseItem(self, response):
        title = response.xpath("//body/div[@id='p-box']/div/div"
                            "[@id='product-intro']/div/div/"
                            "div/h1/text()").extract()
        img_url = response.xpath("//body/div[@id='p-box']"
                                "/div/div[@id='product-intro']"
                                "/div[@id='preview']/div[@id='spec-n1']"
                                "/img/@src").extract()
        if len(title)!=0 and len(img_url)!=0:
            title=title[0].strip()
            logging.info(title)
            img_url = "http://"+img_url[0][2:]
            logging.info(img_url)
            imge_name = os.path.basename(img_url)
            file_path=os.path.join(IMAGE_PATH,imge_name)
            with urlopen(img_url) as image_fd:
                with open(file_path,'wb') as file_fd:
                    file_fd.write(image_fd.read())
            return JdbookscrapyItem(name='bookInfo',
                        book_name=title, image_location=file_path)
        return None
