import scrapy
import json
from scrapy import Request
import re
from delivery_reviews.items import DeliveryReviewsItem


def get_urls():
    with open('delivery_reviews/spiders/shops.txt', "r") as f:
        return [f'{url.strip()}/feedbacks' for url in f.readlines()]


class StockCatalogSpider(scrapy.Spider):
    name = 'reviews'
    start_urls = get_urls()
    reg = r'chainId\":\"\d+'
    url = 'https://api.delivery-club.ru/api1.2/reviews?chainId={chainId}&limit=20&offset={offset}'

    def parse(self, response):
        text = response.xpath('.//script[contains(text(), ("chainId"))]/text()').get()
        chainId = int(re.findall(self.reg, text)[0].lstrip('chainId": "'))

        yield Request(
            url=self.url.format(offset=0, chainId=chainId),
            callback=self.parse_json,
            meta={'offset': 0,
                  'chainId': chainId}
        )

    def parse_json(self, response):
        data = json.loads(response.body)
        chainId = response.meta['chainId']
        offset = response.meta['offset']
        offset += 20

        for review in data['reviews']:
            item = DeliveryReviewsItem()
            if review:
                item['author'] = review["author"]
                item['body'] = review["body"]
                item['rated'] = review["rated"]
                yield item

            yield Request(
                url=self.url.format(offset=offset, chainId=chainId),
                meta={'offset': offset, 'chainId': chainId},
                callback=self.parse_json,
            )
