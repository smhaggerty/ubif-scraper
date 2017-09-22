# -*- coding: utf-8 -*-
import scrapy
from time import ctime
from scrapy.spiders import Spider

class URLItem(scrapy.Item):
    url = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()

# TODO: ipod and computer-repair craw does not reach proper depth, search for "computer-repair" and "ipod" in output file
class MainSpider(Spider):
    name = "main"
    allowed_domains = ['www.ubreakifix.com']
    start_urls = ['https://www.ubreakifix.com/iphone-repair',
                  'https://www.ubreakifix.com/google-repair',
                  'https://www.ubreakifix.com/samsung-repair',
                  'https://www.ubreakifix.com/lg-repair',
                  'https://www.ubreakifix.com/htc-repair',
                  'https://www.ubreakifix.com/motorola-repair',
                  'https://www.ubreakifix.com/blackberry-repair',
                  'https://www.ubreakifix.com/nokia-repair',
                  'https://www.ubreakifix.com/amazon-repair',
                  'https://www.ubreakifix.com/game-console-repair',
                  'https://www.ubreakifix.com/ipod-repair',
                  'https://www.ubreakifix.com/tablet-repair',
                  'https://www.ubreakifix.com/computer-repair']

    def parse(self, response):
        urls = response.xpath('/html/body/div[6]/div[1]/div[2]/section/div/div[2]/div[2]/div/div/a/@href').extract()
        if urls == []:
            yield self.parse_repair_page(response)
        else:
            for url in urls:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse_repair_page(self, response):
        price = response.css('.product-price::text').extract_first()
        item = URLItem()
        item['url'], item['price'], item['date'] = response.url, price, ctime()
        return item