import json

import scrapy

from ..items import LookItem


class InfoSpider(scrapy.Spider):
    name = 'info'

    allowed_domains = ["www.lookfantastic.com.hk"]

    try:
        with open('look/links/electrical.json') as f:
            links = list(map(lambda each: each['link'], json.load(f)))
    except FileNotFoundError:
        links = list()

    def start_requests(self):
        for start_url in self.links:
            yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        item = LookItem()
        no_data = '-'
        try:
            item['name'] = ' '.join(response.xpath('.//h1[@class="product-title font-alpha"]/text()').extract_first().split()[1:])
        except:
            item['name'] = no_data
        item['product_url'] = response.url
        try:
            item['brand'] = response.xpath('.//div[@class="product-more-details"]').xpath('.//tr[@class="odd"]/td/ul/li/text()').extract_first().strip()
        except:
            item['brand'] = no_data
        try:
            item['price'] = response.xpath('.//span[@class="price"]/text()').extract_first().strip()
        except:
            item['price'] = no_data
        description = list()
        try:
            for each_p in response.xpath('.//div[@itemprop="description"]').xpath('.//p'):
                if each_p.xpath('text()').extract():
                    description.append(each_p.extract().replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '').replace('<br>', '').replace('<em>', '').replace('</em>', ''))
        except:
                pass
        try:
            item['product_description'] = '\n'.join(description)
        except:
            item['product_description'] = no_data
        try:
            item['image_url'] = response.xpath('.//img[@class="product-img"]/@src').extract_first()
        except:
            item['image_url'] = no_data
        colour = list()
        try:
            for each_o in response.xpath('.//select[@id="opts-4"]').xpath('.//option'):
                colour.append(each_o.xpath('text()').extract_first().strip())
        except:
            pass
        try:
            item['colour'] = ', '.join(colour[1:])
        except:
            item['colour'] = no_data
        yield item
