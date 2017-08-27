import json
import re

from scrapy import Selector
from selenium import webdriver

from ..items import InfoItem
import scrapy


class GetInfoSpider(scrapy.Spider):
    name = "get_info"

    allowed_domains = ["beautylish.com"]

    # try:
    #     with open('links_fragrance.json') as f:
            # start_urls = list(map(lambda i: 'https://www.beautylish.com%s' % i['link'], json.load(f)))
    # except FileNotFoundError:
        # start_urls = list()
    start_urls = ['https://www.beautylish.com/s/oribe-gold-lust-repair-and-restore-conditioner-1-l']

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
        self.driver.get(response.url)
        selenium_response_text = self.driver.page_source
        response = Selector(text=selenium_response_text)
        sizes = list(map(lambda i: 'https://www.beautylish.com%s' % i, response.xpath('.//a[@class="thumbList_link"]/@href').extract()))

        no_item = '-'
        item = InfoItem()
        try:
            item['brand'] = response.xpath('.//h3[@itemprop="brand"]/a/text()').extract_first()
        except:
            item['brand'] = no_item
        try:
            item['title'] = response.xpath('.//h1[@itemprop="name"]/text()').extract_first()
        except:
            item['title'] = no_item
        try:
            item['price'] = response.xpath('.//h4/span/text()').extract_first()
        except:
            item['price'] = no_item
        try:
            item['catalogs'] = ','.join(response.xpath('.//li[@itemscope="itemscope"]/a/span/text()').extract())
        except:
            item['catalogs'] = no_item
        try:
            item['short_description'] = response.xpath('.//small[@class="block mb20"]/text()').extract_first().strip()
        except:
            item['short_description'] = no_item
        try:
            initial = response.xpath('.//div[@id="desc-tab-content"]').extract_first().strip().replace('\n\n', '\n')
            without_tag = re.sub(r'\<[^>]*\>', '', initial)
            item['description'] = without_tag
        except:
            item['description'] = no_item
        try:
            image_left = ',\n'.join(list(map(lambda i: 'http:%s' % i.replace('85x85', '550x550'), response.xpath('.//ul[@class="thumb_list"]').xpath('.//li/img/@src').extract())))
        except:
            image_left = False
        try:
            image_right = ',\n'.join(list(map(lambda i: 'http:%s' % i.replace('35x35', '550x550'), response.xpath('.//img[@class="thumbList_img"]/@src').extract())))
        except:
            image_right = False
        if image_left:
            item['image_url'] = image_left
        elif image_right:
            item['image_url'] = image_right
        elif image_left and image_right:
            item['image_url'] = ',\n'.join([image_left, image_right])
        else:
            item['image_url'] = no_item
        yield item
        self.driver.close()

