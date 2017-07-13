# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinksItem(scrapy.Item):
    link = scrapy.Field()


class BayItem(scrapy.Item):
    id = scrapy.Field()
    brand = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    colour = scrapy.Field()
    product_description = scrapy.Field()
    meta_tag = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
