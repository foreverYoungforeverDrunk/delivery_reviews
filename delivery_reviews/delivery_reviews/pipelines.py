import pymongo

from scrapy.utils.project import get_project_settings


class DeliveryReviewsPipeline:

    def __init__(self):
        settings = get_project_settings()
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'],
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
