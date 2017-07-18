from time import sleep

from scrapy import Selector

from ..items import CatalogsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from selenium import webdriver
import scrapy
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select


class CatalogsSpider(scrapy.Spider):
    name = "catalogs"

    allowed_domains = ["www.walgreens.com"]

    start_urls = ['https://www.walgreens.com/store/store/category/productlist.jsp?N=360457&Eon=360457&No=0&Erp=72&']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # self.display = Display(visible=0, size=(1024, 768))
        # self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            try:
                selenium_response_text = self.driver.page_source
                new_selector = Selector(text=selenium_response_text)
                for each in new_selector.css('a[id*="title-secondary-"]'):
                    item = CatalogsItem()
                    item['link'] = each.css('::attr(href)').extract()
                    yield item
                next_page = self.driver.find_element_by_id('omni-next-click')
                next_page.click()
            except:
                break
        self.driver.close()
        # self.display.stop()
