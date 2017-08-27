# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeautylishItem(scrapy.Item):
    link = scrapy.Field()


class CatalogsItem(scrapy.Item):
    catalog = scrapy.Field()


class InfoItem(scrapy.Item):
    brand = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    catalogs = scrapy.Field()
    short_description = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()


class SizesItem(scrapy.Item):
    url = scrapy.Field()
