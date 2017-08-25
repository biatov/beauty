from ..items import WalgreensItem
import scrapy
from scrapy import Selector
import re

from multiprocessing import Pool

from selenium import webdriver
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
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Chrome()

    def parse(self, response):

        try:
            with open('walgreens/links/bathandbody.json') as f:
                paginate = list(map(lambda each: each['link'][0], json.load(f)))
        except FileNotFoundError:
            paginate = list()

        try:
            with open('walgreens/info/bathandbody/brands.json') as f:
                brands = json.load(f)[0]['brands']
        except FileNotFoundError:
            brands = list()

        no_data = '-'
        for each in paginate:
            try:
                self.driver.get('https://www.walgreens.com%s' % each)
            except:
                continue
            try:
                element = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "proImg"))
                )
            except:
                continue
            try:
                selenium_response_text = self.driver.page_source
                new_selector = Selector(text=selenium_response_text)
            except:
                continue
            item = WalgreensItem()
            try:
                name = new_selector.xpath('.//span[@itemprop="name"]/text()').extract_first()
                if not name:
                    name = new_selector.xpath('.//span[@itemprop="name"]/text()').extract()
            except:
                name = no_data
            brand = ''
            for each_b in brands:
                if each_b in name:
                    name = name.replace(each_b, '').strip()
                    brand = each_b
            try:
                item['name'] = name
            except:
                item['name'] = no_data
            try:
                item['brand'] = brand.strip()
            except:
                item['brand'] = no_data
            try:
                item['price'] = new_selector.xpath('.//span[@class="sr-only ng-binding ng-scope"]/text()').extract_first()
            except:
                item['price'] = no_data
            colour = list()
            try:
                for each_c in new_selector.xpath('.//ul[@ng-if="productModel.colorAvailble"]').xpath('li'):
                    colour.append(each_c.xpath('.//a/@data-content').extract_first().strip())
            except:
                continue
            try:
                item['colour'] = ', '.join(colour)
            except:
                item['colour'] = no_data
            try:
                initial = new_selector.xpath('.//div[@id="descriptionContentPlaceHolder"]').extract_first().replace('\n\n', '\n')
                init_split = initial.split('<script>')
                try:
                    all_part = ''.join([init_split[0], init_split[1].split('</script>')[1]]).replace('\n\n', '\n')
                except:
                    all_part = initial.replace('\n\n', '\n')
                without_tag = re.sub(r'\<[^>]*\>', '', all_part).replace('\n\n', '\n')
                item['description'] = without_tag
            except:
                item['description'] = no_data
            try:
                item['product_url'] = 'https://www.walgreens.com%s' % each
            except:
                item['product_url'] = no_data
            try:
                item['image_url'] = 'http:%s' % new_selector.xpath('.//img[@id="proImg"]/@src').extract_first()
            except:
                item['image_url'] = no_data
            yield item
        try:
            self.driver.close()
        except:
            pass
        self.display.stop()