import os

from scrapy import Request
from scrapy import Selector
from ..items import LinksItem
import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"

    allowed_domains = ["beautybay.com"]

    catalogs = ["/cosmetics/", "/makeupbrushes/", "/skincare/", "/bathandbody/", "/haircare/", "/nailcare/",
                "/electrical/", "/accessories/"]

    start_urls = ['http://beautybay.com/accessories/']

    def parse(self, response):

        next_page = response.xpath('.//a[@id="next-page"]/@href').extract_first()
        root = Selector(response)

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        for each in root.xpath('.//div[@class="o-lister"]').xpath('.//div[@class="o-lister__item"]'):
            item = LinksItem()
            item['link'] = each.xpath('.//a[@class="c-product qa-product"]/@href').extract()
            yield item
