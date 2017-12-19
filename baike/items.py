# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikeItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    wordid = scrapy.Field()
    polysemy = scrapy.Field()
    synonym = scrapy.Field()
    summary = scrapy.Field()
    summarylinks = scrapy.Field()

    basicinfo = scrapy.Field()

    content = scrapy.Field()
    contentlinks = scrapy.Field()

    relword = scrapy.Field()
