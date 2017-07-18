from ..items import WalgreensItem
import scrapy
from scrapy import Selector
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

import json


class InfoSpider(scrapy.Spider):
    name = "info"

    allowed_domains = ["www.walgreens.com"]

    start_urls = ['http://www.walgreens.com']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # self.display = Display(visible=0, size=(1024, 768))
        # self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):

        # try:
        #     with open('walgreens/links/cosmetics/eyes.json') as f:
        #         paginate = list(map(lambda each: each['link'][0], json.load(f)))
        # except FileNotFoundError:
        #     paginate = list()

        paginate = ['/store/c/milani-brow-fix-brow-kit/ID=prod6107707-product']
        no_data = '-'
        brands = ['Milani']
        for each in paginate:
            self.driver.get('https://www.walgreens.com%s' % each)
            selenium_response_text = self.driver.page_source
            new_selector = Selector(text=selenium_response_text)
            item = WalgreensItem()
            try:
                name = new_selector.xpath('.//span[@itemprop="name"]/text()').extract_first()
            except:
                name = no_data
            item['brand'] = ''
            for each_b in brands:
                if each_b in name:
                    name = name.replace(each_b, '').strip()
                    brand = each_b
            item['name'] = name
            item['brand'] = brand
            try:
                item['price'] = new_selector.xpath('.//span[@class="sr-only ng-binding ng-scope"]/text()').extract_first()
            except:
                item['price'] = no_data
            colour = list()
            try:
                for each_c in new_selector.xpath('.//ul[@ng-if="productModel.colorAvailble"]').xpath('li'):
                    colour.append(each_c.xpath('.//a/@data-content').extract_first().strip())
            except:
                pass
            try:
                item['colour'] = ', '.join(colour)
            except:
                item['colour'] = no_data
            try:
                initial = new_selector.xpath('.//div[@id="descriptionContentPlaceHolder"]').extract_first()
                init_split = initial.split('<script>')
                all_part = ''.join([init_split[0], init_split[1].split('</script>')[1]]).replace('<p>', '\n')
                without_tag = re.sub(r'\<[^>]*\>', '', all_part)
                item['description'] = without_tag
            except:
                item['description'] = no_data
            item['product_url'] = 'https://www.walgreens.com%s' % each
            try:
                item['image_url'] = 'http:%s' % new_selector.xpath('.//img[@id="proImg"]/@src').extract_first()
            except:
                item['image_url'] = no_data
            yield item
        self.driver.close()
        # self.display.stop()