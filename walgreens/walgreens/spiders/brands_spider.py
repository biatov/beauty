from scrapy import Selector

from ..items import BrandsItem
from selenium import webdriver
import scrapy
from pyvirtualdisplay import Display


class BrandsSpider(scrapy.Spider):
    name = "brands"

    allowed_domains = ["www.walgreens.com"]

    start_urls = ['https://www.walgreens.com/store/c/productlist/N=360337/1/ShopAll=360337']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # self.display = Display(visible=0, size=(1024, 768))
        # self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        for i in self.driver.find_elements_by_xpath('.//a[@title="view more"]'):
            i.click()
        # for each in self.driver.find_elements_by_link_text('View more'):
        #     each.click()
        selenium_response_text = self.driver.page_source
        new_selector = Selector(text=selenium_response_text)
        item = BrandsItem()
        item['brands'] = new_selector.xpath('.//section[@id="Brand"]').xpath('.//span[@class="wag-text-grey ng-binding"]').xpath('text()').extract()
        yield item
        self.driver.close()
        # self.display.stop()
