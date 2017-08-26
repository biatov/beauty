import json

from ..items import InfoItem
import scrapy


class GetInfoSpider(scrapy.Spider):
    name = "get_info"

    allowed_domains = ["beautylish.com"]

    try:
        with open('links_fragrance.json') as f:
            start_urls = list(map(lambda i: 'https://www.beautylish.com%s' % i['link'], json.load(f)))
    except FileNotFoundError:
        start_urls = list()

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, headers={'Referer': 'https://www.beautylish.com/'})

    def parse(self, response):
        item = InfoItem()
        item['brand'] = response.xpath('.//h3[@itemprop="brand"]/a/text()').extract_first()
        item['title'] = response.xpath('.//h1[@itemprop="name"]/text()').extract_first()
        item['price'] = response.xpath('.//h4/span/text()').extract_first()
        item['catalogs'] = ', '.join(response.xpath('.//li[@itemscope="itemscope"]/a/span/text()').extract())
        yield item

