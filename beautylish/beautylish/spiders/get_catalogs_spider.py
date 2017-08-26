import re

from ..items import CatalogsItem
import scrapy


class GetCatalogsSpider(scrapy.Spider):
    name = "get_catalogs"

    allowed_domains = ["beautylish.com"]

    start_urls = ['https://www.beautylish.com/']

    def parse(self, response):

        for each in response.xpath('.//a[@class="catMenu_trigger catMenu_title js-menu-trigger"]'):
            item = CatalogsItem()
            check = each.xpath('@href').extract_first()
            if re.search('[?=]', check):
                item['catalog'] = 'https://www.beautylish.com%s' % check
                yield item
