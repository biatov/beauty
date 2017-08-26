import json

from ..items import BeautylishItem
import scrapy


class GetPagesSpider(scrapy.Spider):
    name = "get_pages"

    allowed_domains = ["beautylish.com"]

    try:
        with open('catalogs.json') as f:
            start_url = list(map(lambda i: i['catalog'], json.load(f)))
    except FileNotFoundError:
        start_url = list()

    start_urls = [start_url[4]]

    def parse(self, response):
        next_page = response.xpath('.//span[@class="pager_next"]/a/@href').extract_first()

        if next_page:
            next_page = 'https://www.beautylish.com%s' % next_page
            yield scrapy.Request(next_page, callback=self.parse)

        for each in response.xpath('.//ul[@class="small_tile_2 medium_tile_3 mb20"]').xpath('.//li'):
            item = BeautylishItem()
            item['link'] = each.xpath('a/@href').extract_first()
            yield item
