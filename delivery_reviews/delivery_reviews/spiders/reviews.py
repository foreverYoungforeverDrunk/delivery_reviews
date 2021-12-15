import scrapy
import json
from scrapy import Request


class StockCatalogSpider(scrapy.Spider):
    name = 'burger'
    start_urls = ['https://www.delivery-club.ru/srv/Burger_King_grval/feedbacks']
    url = 'https://api.delivery-club.ru/api1.2/reviews?chainId=15275&limit={limit}&offset={offset}'

    def parse(self, response):
        yield Request(
            url=self.url.format(limit=20, offset=0),
            callback=self.parse_json,
            meta={'offset': 0},
        )

    def parse_json(self, response):
        data = json.loads(response.body)
        offset = response.meta['offset']
        offset += 20

        for review in data['reviews']:
            if review:
                yield {
                    "author": review["author"],
                    "body": review["body"],
                    "rated": review["rated"],
                }

                yield Request(
                    url=self.url.format(limit=20, offset=offset),
                    meta={'offset': offset},
                    callback=self.parse_json,
                )
