import re
import json

import scrapy
from scrapy import Selector

from ..items import InfoItem
from selenium import webdriver


class GetInfoSpider(scrapy.Spider):
    name = 'get_info'

    allowed_domains = ['www.ulta.com']

    start_urls = ['http://www.ulta.com']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        try:
            with open('ulta/links/makeup_ultacolection.json') as f:
                start_urls = list(map(lambda i: 'http://www.ulta.com%s' % i['link'], json.load(f)))
        except FileNotFoundError:
            start_urls = list()
        for each in start_urls:
            try:
                self.driver.get(each)
            except:
                pass
            selenium_response_text = self.driver.page_source
            response = Selector(text=selenium_response_text)
            item = InfoItem()
            no_item = '-'
            try:
                item['title'] = response.xpath('.//h1[@itemprop="name"]/text()').extract_first().strip()
            except:
                item['title'] = no_item
            try:
                item['brand'] = response.xpath('.//h2[@itemprop="brand"]/a/text()').extract_first()
            except:
                item['brand'] = no_item
            try:
                item['price'] = response.xpath('.//p[@id="skuInfoPrice"]/text()').extract_first().strip()
            except:
                item['price'] = no_item
            try:
                image = ',\n'.join(list(map(lambda i: i.split('?')[0] if i[0] != '/' else 'http:%s' % i.split('?')[0], response.xpath('.//li[contains(@class, "thumbnail-image-pdp")]/a/img/@src').extract())))
            except:
                image = ''
            if image:
                item['image'] = image
            else:
                try:
                    item['image'] = response.xpath('.//div[@class="s7staticimage"]/img/@src').extract_first().split('?')[0]
                except:
                    item['image'] = response.xpath('.//div[@class="s7staticimage"]/img/@src').extract_first()
            try:
                sub_title = response.xpath('.//div[@class="color-panel"]/ul').xpath('.//li/a//img/@alt').extract()
                sub_title = list(map(lambda i: i.replace(item['title'], '').replace(item['brand'], '').strip() ,sub_title))
            except:
                sub_title = ''
            if sub_title:
                item['sub_title'] = ', '.join(sub_title)
            else:
                item['sub_title'] = ''
            try:
                initial = response.xpath('.//div[@class="product-catalog-content current-longDescription"]').extract_first().strip().replace('\n\n', '\n').replace('\t', '').replace('</li><li>', '; ')
                without_tag = re.sub(r'\<[^>]*\>', '', initial)
                item['description'] = without_tag
            except:
                item['description'] = ''
            item['url'] = each
            try:
                item['catalogs'] = ', '.join(response.xpath('.//div[@class="makeup-breadcrumb"]/ul').xpath('.//li/a/text()').extract()[1:])
            except:
                item['catalogs'] = no_item
            yield item
        self.driver.close()
