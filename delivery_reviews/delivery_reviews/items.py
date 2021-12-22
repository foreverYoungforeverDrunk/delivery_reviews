import scrapy


class DeliveryReviewsItem(scrapy.Item):
    author = scrapy.Field()
    body = scrapy.Field()
    rated = scrapy.Field()
