from ..items import BayItem
import scrapy
from scrapy import Selector

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

import json


class InfoSpider(scrapy.Spider):
    name = "info"

    allowed_domains = ["beautybay.com"]

    start_urls = ['http://beautybay.com']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):

        try:
            with open('bay/json/nailcare.json') as f:
                paginate = list(map(lambda each: each['link'][0], json.load(f)))
        except FileNotFoundError:
            paginate = list()

        self.driver.get(response.url)
        self.driver.find_element_by_id('nav-account').click()
        self.driver.find_element_by_xpath('.//a[@class="js-region-settings"]').click()
        delivery = Select(self.driver.find_element_by_id('region-delivery'))
        delivery.select_by_visible_text('Hong Kong')
        currency = Select(self.driver.find_element_by_id('region-currency'))
        currency.select_by_value('11')
        self.driver.find_element_by_xpath('.//form[@id="region-settings"]/input[@class="btn action btn-block"]').submit()

        no_data = '-'
        count = 1
        for each in paginate:
            self.driver.get('http://beautybay.com%s' % each)
            # sleep(1)
            try:
                element = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "selected-image"))
                )
            except:
                pass
            selenium_response_text = self.driver.page_source
            new_selector = Selector(text=selenium_response_text)
            item = BayItem()
            item['id'] = count
            try:
                item['brand'] = new_selector.xpath('.//div[@class="product-info"]').xpath('.//a/text()').extract_first()
            except:
                item['brand'] = no_data
            try:
                item['product_name'] = new_selector.xpath('.//div[@class="product-info"]').xpath('.//span[@class="product-title"]/text()').extract_first()
            except:
                item['product_name'] = no_data
            try:
                item['price'] = new_selector.xpath('.//span[@class="product-price"]/text()').extract_first()
            except:
                item['price'] = no_data
            colour = list()
            try:
                for each_o in new_selector.xpath('.//select[@id="group-sku"]').xpath('.//option'):
                        colour.append(each_o.xpath('text()').extract_first().strip())
            except:
                pass
            try:
                item['colour'] = ',\n'.join(colour[1:])
            except:
                item['colour'] = no_data
            description = list()
            try:
                for each_p in new_selector.xpath('.//div[re:test(@class, "product-description")]').xpath('.//p'):
                    if each_p.xpath('text()').extract_first():
                        description.append(each_p.xpath('text()').extract_first().strip())
            except:
                pass
            try:
                item['product_description'] = '\n'.join(description)
            except:
                item['product_description'] = no_data
            item['product_url'] = 'http://beautybay.com%s' % each
            try:
                item['image_url'] = 'http:%s' % new_selector.xpath('.//a[@id="selected-image"]/img/@src').extract_first().split('?')[0]
            except:
                item['image_url'] = no_data
            count += 1
            yield item

        self.driver.close()
        self.display.stop()

