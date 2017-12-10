#!/bin/bash
cd /home/scott/github/my_mini_project/monitor_baidu_finance_news/baidunews
source /usr/local/bin/virtualenvwrapper.sh
workon scrapy
scrapy crawl finance_news 2>> /home/scott/tmp/baidu_news.log
