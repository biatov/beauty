# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatalogsItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()


class WalgreensItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    colour = scrapy.Field()
    description = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()


class BrandsItem(scrapy.Item):
    brands = scrapy.Field()
