# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinksItem(scrapy.Item):
    link = scrapy.Field()


class LookItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    product_url = scrapy.Field()
    price = scrapy.Field()
    product_description = scrapy.Field()
    image_url = scrapy.Field()
    colour = scrapy.Field()

