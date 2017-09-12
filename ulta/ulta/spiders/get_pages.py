import scrapy

from ..items import PagesItem


class GetPages(scrapy.Spider):
    name = 'get_pages'

    allowed_domains = ['www.ulta.com']

    start_urls = ['http://www.ulta.com/makeup-ulta-collection?N=26zi']

    def parse(self, response):
        next_page = response.xpath('.//li[@class="next-prev floatl-span"]/a[contains(.//text(), "Next")]/@href').extract_first()

        if next_page:
            next_page = 'http://www.ulta.com%s' % next_page
            yield scrapy.Request(next_page, callback=self.parse)

        for each in response.xpath('.//ul[@id="foo16"]').xpath('.//li'):
            item = PagesItem()
            item['link'] = each.xpath('div[@class="productQvContainer"]/h4/a/@href').extract_first()
            yield item
