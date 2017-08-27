import json
import re

from scrapy import Selector
from selenium import webdriver

from ..items import SizesItem
import scrapy


class GetSizesSpider(scrapy.Spider):
    name = "get_sizes"

    allowed_domains = ["beautylish.com"]

    try:
        with open('links_hair.json') as f:
            start_urls = list(map(lambda i: 'https://www.beautylish.com%s' % i['link'], json.load(f)))
    except FileNotFoundError:
        start_urls = list()
    # start_urls = ['https://www.beautylish.com/s/oribe-gold-lust-repair-and-restore-conditioner-1-l']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        PROXY = "119.9.105.210"
        PORT = 9000
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.https", PROXY)
        profile.set_preference("network.proxy.http_port", PORT)
        profile.set_preference("network.proxy.ssl", PROXY)
        profile.set_preference("network.proxy.ssl_port", PORT)
        self.driver = webdriver.Firefox(firefox_profile=profile)

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, headers={'Referer': 'https://www.beautylish.com/'})

    def parse(self, response):
        new_url = response.url
        self.driver.get(new_url)
        selenium_response_text = self.driver.page_source
        response = Selector(text=selenium_response_text)

        check = response.xpath('.//a[@class="thumbList_link"]')

        item = SizesItem()
        if check:
            for each in response.xpath('.//a[@class="thumbList_link"]'):
                item['url'] = 'https://www.beautylish.com%s' % each.xpath('@href').extract_first()
                yield item
        else:
            item['url'] = new_url
            yield item
        self.driver.close()

