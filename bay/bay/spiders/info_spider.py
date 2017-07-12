import json
from time import sleep

from scrapy import Request
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from ..items import BayItem
import scrapy


class InfoSpider(scrapy.Spider):
    name = "info"

    allowed_domains = ["beautybay.com"]

    start_urls = ['http://beautybay.com']

    # def start_requests(self):
    #     for start_url in self.start_urls:
    #         yield Request(url=start_url, headers={'Referer': 'http://beautybay.com/'})

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.driver = webdriver.Firefox()

    def parse(self, response):

        try:
            with open('nailcare.json') as f:
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
        for each in paginate:
            self.driver.get('http://beautybay.com%s' % each)
            sleep(5)
            selenium_response_text = self.driver.page_source
            new_selector = Selector(text=selenium_response_text)
            item = BayItem()
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
                for each in new_selector.xpath('.//select[@id="group-sku"]').xpath('.//option'):
                        colour.append(each.xpath('text()').extract_first().strip())
            except:
                pass
            try:
                item['colour'] = ',\n'.join(colour[1:])
            except:
                item['colour'] = no_data
            description = list()
            try:
                for each in new_selector.xpath('.//div[re:test(@class, "product-description expander")]').xpath('.//p'):
                    if each.xpath('text()').extract_first():
                        description.append(each.xpath('text()').extract_first().strip())
            except:
                pass
            try:
                item['product_description'] = '\n'.join(description)
            except:
                item['product_description'] = no_data
            try:
                item['meta_tag'] = new_selector.xpath('.//div[@id="curalate-no-content"]').xpath('.//strong/text()').re_first(r'#\w+')
            except:
                item['meta_tag'] = no_data
            yield item

        self.driver.close()

