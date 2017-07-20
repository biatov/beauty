from pyvirtualdisplay import Display
from scrapy import Selector

from ..items import CatalogsItem
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CatalogsSpider(scrapy.Spider):
    name = "links"

    allowed_domains = ["www.walgreens.com"]

    start_urls = ['https://www.walgreens.com/store/store/category/productlist.jsp?N=360337/1/ShopAll=360337&Eon=360337/1/ShopAll=360337&Erp=72&']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # self.display = Display(visible=0, size=(1024, 768))
        # self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            try:
                try:
                    element = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.ID, "proImg"))
                    )
                except:
                    pass
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
