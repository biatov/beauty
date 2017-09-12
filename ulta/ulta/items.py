# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PagesItem(scrapy.Item):
    link = scrapy.Field()


class SizesItem(scrapy.Item):
    url = scrapy.Field()


class InfoItem(scrapy.Item):
    title = scrapy.Field()
    sub_title = scrapy.Field()
    brand = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    catalogs = scrapy.Field()
