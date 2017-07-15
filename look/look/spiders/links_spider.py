from ..items import LinksItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class LinksSpider(CrawlSpider):
    name = "link"

    allowed_domains = ["www.lookfantastic.cn"]

    start_urls = ['https://www.lookfantastic.com.hk/health-beauty/electrical/view-all-electrical.list']

    # https://www.lookfantastic.cn/home.dept?settingsSaved=Y&shippingcountry=HK&switchcurrency=CNY&countrySelected=Y

    rules = [
        Rule(LinkExtractor
             (allow=('/health\-beauty\/electrical\/view\-all\-electrical\.list\?pageNumber=\d+')),
             callback='parse_item',
             follow=True
             )
    ]

    def parse_item(self, response):
        selector = response.css('div[id*="divSearchResults"]').xpath('.//p[@class="product-name item_productTitle"]')
        for each in selector:
            item = LinksItem()
            item['link'] = each.xpath('.//a/@href').extract_first()
            yield item

