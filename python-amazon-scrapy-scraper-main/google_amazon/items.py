# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from itemloaders.processors import MapCompose, Identity, Join, Compose
import re


def price_to_float(values):
    try:
        values = ".".join(values).replace(",", "")
        return float(values)
    except ValueError:
        return None

# def filter_images(image_url):
#     if "overlay" in image_url:
#         return None
#     if "button" in image_url:
#         return None
#     return re.sub(r"_.*\..*", "AC_UL1500_.jpg", image_url)
#     # return re.sub(r"AC.*", "AC_UL1500_.jpg", image_url)

def discount_to_float(discount_str):
    try:
        return float(discount_str.replace("%", ""))
    except:
        return 0

class SearchResultItem(Item):
    # define the fields for your item here like:
    search_term_id = Field()
    search_term = Field()
    name = Field()
    asin = Field()
    url = Field()
    amazon_search_url = Field()
    star_rating = Field(input_processor=MapCompose(float))
    num_of_ratings = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    price = Field(output_processor=lambda v: price_to_float(v))
    currency = Field()
    discount_pct = Field(input_processor=MapCompose(discount_to_float))
    # for downloading images
    images = Field()
    # change the image url to the high quality one
    image_urls = Field(output_processor=Identity())


class AmazonAsinItem(Item):
    name = Field()
    asin = Field()
    keyword_id = Field()
    page_id = Field()
    price = Field(output_processor=Compose(Join("."), float))
    url = Field()
    features = Field(output_processor=Join("$$$"))
    colors = Field(output_processor=Join("$$$"))
    total_ratings = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    image_urls = Field(output_processor=Identity())
    images = Field()
    average_rating = Field(input_processor=MapCompose(float))
    brand = Field(input_processor=MapCompose(lambda x: re.sub(r"(^Visit\sthe\s|^Brand:\s|\sStore$)", "", x)))
    brand_url = Field()
    details = Field()
    best_seller_rank = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    best_seller_category = Field()
    other_category_rank = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    other_category = Field()
    description = Field(input_processor=MapCompose(str.strip), output_processor=Compose(Join()))
    reviews = Field(output_processor=Identity())
    questions = Field(output_processor=Identity())
    is_valid_asin = Field()

    
class AmazonReviewItem(Item):
    header = Field()
    body = Field(input_processor=MapCompose(lambda x: x.strip()), output_processor=Compose(Join()))
    review_date = Field()
    related_item_id = Field()
    reviewer = Field()
    purchase_type = Field()
    reviewer_location = Field()
    reviewer_rating = Field(input_processor=MapCompose(float))

class AmazonQuestionItem(Item):
    body = Field(input_processor=MapCompose(lambda x: x.strip()), output_processor=Compose(Join()))
    answer = Field(input_processor=MapCompose(lambda x: x.strip()), output_processor=Compose(Join()))
    related_item_id = Field()
    num_of_votes = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    num_of_answers = Field(input_processor=MapCompose(lambda x: x.replace(",", ""), int))
    date_answered = Field()
    answered_by = Field()