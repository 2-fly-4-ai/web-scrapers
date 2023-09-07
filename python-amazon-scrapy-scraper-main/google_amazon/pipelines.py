from urllib.parse import urlparse
import re
from os.path import splitext
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from scrapy.exporters import CsvItemExporter
from pathlib import Path
from google_amazon.models import create_table, SearchResult, Image, Asin, Review, AmazonQuestion
import pymongo

class AmazonImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        parsed_url = urlparse(item.get("url"))
        canonical = re.match(r"\/(.*)\/dp.*", parsed_url.path).group(1)
        image_number = item.get("image_urls").index(request.url) + 1
        asin = item.get("asin")
        extension = splitext(request.url.split('/')[-1])[-1]
        return f"{asin}-{canonical}-{image_number}{extension}"

class PerFilenameExportPipeline:
    """Distribute items across multiple CSV files according to their 'search_term' field"""
    def __init__(self, fields_to_export):
        self.fields_to_export = fields_to_export

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            fields_to_export=crawler.settings.get('FEED_EXPORT_FIELDS'),
        )

    def open_spider(self, spider):
        self.filename_to_exporter = {}
        self.scraping_date = spider.scraping_date
        Path(f'scraped_data/{self.scraping_date}').mkdir(parents=True, exist_ok=True)

    def close_spider(self, spider):
        for exporter in self.filename_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        filename = f'{item.get("search_term_id")}-{item.get("search_term").strip().replace("/", "_")}'
        if filename not in self.filename_to_exporter:
            f = open(f'scraped_data/{self.scraping_date}/{filename}.csv', 'wb')
            exporter = CsvItemExporter(f)#, fields_to_export = self.fields_to_export)
            exporter.start_exporting()
            self.filename_to_exporter[filename] = exporter
        return self.filename_to_exporter[filename]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

class PostgresDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def __init__(self, settings) -> None:
        hostname = settings.get("DATABASE_HOST")
        username = settings.get("DATABASE_USER")
        password = settings.get("DATABASE_PASSWORD")
        database = settings.get("DATABASE_NAME")
        port = settings.get("DATABASE_PORT", '5432')

        # connection string
        db_uri = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
        engine = create_engine(db_uri)
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def close_spider(self, spider):
        self.Session.close_all()

    def process_item(self, item, spider):
        # convert item into adapter for easier use
        adapter = ItemAdapter(item)

        # get the images so you can insert them into their own table
        images = adapter.get("images")
        if images is not None:
            del adapter["images"]

        # get reviews and then insert into their own table
        reviews = adapter.get("reviews")
        if reviews is not None:
            del adapter["reviews"]

        # get questions and then insert into their own table
        questions = adapter.get("questions")
        if questions is not None:
            del adapter["questions"]

        session = self.Session()
        # insert main item into the database
        if spider.name == "search_terms":
            record = SearchResult(**adapter)
        elif spider.name == "asins":
            record = Asin(**adapter)
        
        try:
            session.add(record)
            session.flush()
            item_id = record.id
            session.commit()

            # insert images into images table
            if images:
                for image in images:
                    try:
                        image["related_item_id"] = item_id
                        session.add(Image(**image))
                        session.commit()
                    except IntegrityError as e:
                        session.rollback()
                        spider.logger.error(e._message)

            # insert reviews into the reviews table
            if reviews:
                for review in reviews:
                    try:
                        review["related_item_id"] = item_id
                        session.add(Review(**review))
                        session.commit()
                        del review["related_item_id"]
                    except IntegrityError as e:
                        session.rollback()
                        spider.logger.error(e._message)

            # insert questions into the questions table
            if questions:
                for question in questions:
                    try:
                        question["related_item_id"] = item_id
                        session.add(AmazonQuestion(**question))
                        session.commit()
                        del question["related_item_id"]
                    except IntegrityError as e:
                        session.rollback()
                        spider.logger.error(e._message)


            spider.logger.info(f"Inserted <Item {item_id}> into DB")
        except IntegrityError as e:
            session.rollback()
            spider.logger.error(e._message)


        # close the session
        session.close()

        # add the images list back to the item and return it
        item["images"] = images

        try:
            item["reviews"] = reviews
            item["questions"] = questions
        except:
            pass

        return item


class MongoDBPipeline(object):

    collection_name = None

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        if spider.name == "seach_terms":
            self.collection_name = "search_result"
        if spider.name == "asins":
            self.collection_name = "asin"
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post
        _id = self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        spider.logger.debug(f"<Item {_id.inserted_id}> added to MongoDB database")
        return item
