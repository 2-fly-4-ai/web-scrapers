import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from scrapy.downloadermiddlewares.retry import get_retry_request
from datetime import datetime
from google_amazon.items import AmazonAsinItem, AmazonReviewItem, AmazonQuestionItem
import re
import json
from langdetect import detect

class AsinsSpider(scrapy.Spider):
    name = 'asins'
    allowed_domains = ['amazon.com', 'media-amazon.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'google_amazon.pipelines.AmazonImagesPipeline': 1, # for image downloads
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'google_amazon.middlewares.SmartProxyMiddleware': 100,
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
        }
    }

    def __init__(self, file_name="asins.csv"):
        self.file_name = file_name

    def start_requests(self):
        data = pd.read_csv(self.file_name)
        # rename the columns so that they are valid item names
        data.rename(columns={"Page ID": "PageID", "Keyword ID": "KeywordID"}, inplace=True)
        for row in data.itertuples():
            asins = str(row.ASINs).split(",")
            for asin in asins:
                asin_dict = dict()
                asin_dict["PageID"] = row.PageID
                asin_dict["KeywordID"] = row.KeywordID
                asin_dict["asin"] = asin
                yield scrapy.Request(f"https://www.amazon.com/dp/{asin}", cb_kwargs={'asin_dict': asin_dict}, errback=self.parse_error)

    def parse_error(self, failure):
        if failure.value.response.status == 404:
            # invalid asin
            asin_dict = failure.value.response.cb_kwargs.get("asin_dict")
            loader = ItemLoader(item=AmazonAsinItem(), response=failure.value.response)
            loader.default_output_processor = TakeFirst()
            loader.add_value('asin', asin_dict.get('asin'))
            loader.add_value('keyword_id', asin_dict.get('KeywordID'))
            loader.add_value('page_id',  asin_dict.get('PageID'))
            loader.add_value('is_valid_asin', False)
            
            yield loader.load_item()



    def parse(self, response, asin_dict):        
        # retry the request if the name is missing
        name = response.xpath("normalize-space(//*[@id='productTitle']/text())").get()
        if not name:
            new_request_or_none = get_retry_request(
                response.request,
                spider=self,
                reason='Response is empty',
            )
            if new_request_or_none is not None:
                new_request_or_none.dont_filter = True
                yield new_request_or_none
        else:
            # scrape basic product details
            loader = ItemLoader(item=AmazonAsinItem(), response=response)
            loader.default_output_processor = TakeFirst()
            loader.add_value('name', name)
            loader.add_value('price', response.xpath("//span[@class='a-price-whole']/text()").get())
            loader.add_value('price', response.xpath("//span[@class='a-price-fraction']/text()").get())
            loader.add_value('total_ratings', response.xpath(
                "//*[@id='acrCustomerReviewText']/text()").re_first(r"(.*) ratings"))

            # scrape images
            images = response.xpath("//script/text()").re_first(r"'initial':\s+(\[.*\])")
            images_parsed = json.loads(images)
            # loader.add_xpath('image_urls', "//*[@class='a-button-text']/img[contains(@src,'m.media-amazon.com')]/@src")
            for img in images_parsed:
                image = img.get('hiRes')
                if image is None:
                    image = img.get('large')
                if image is None:
                    image = img.get('main')
                loader.add_value("image_urls", image)

            
            
            loader.add_value('average_rating', response.xpath(
                "//*[@id='acrPopover']/@title").re_first(r"([0-9.]+) out"))
            loader.add_xpath('brand', "//*[@id='bylineInfo']/text()")
            loader.add_value("brand_url", response.urljoin(response.xpath("//*[@id='bylineInfo']/@href").get()))
            loader.add_value('url', response.urljoin(response.xpath("//link[@rel='canonical']/@href").get()))
            loader.add_value('asin', asin_dict.get('asin'))
            loader.add_xpath("colors", "//div[@id='variation_color_name']//img[@class='imgSwatch']/@alt")
            loader.add_value('keyword_id', asin_dict.get('KeywordID'))
            loader.add_value('page_id',  asin_dict.get('PageID'))
            loader.add_value('is_valid_asin', True)
            loader.add_xpath('description', "//h2[contains(text(),'Product Description')]/following-sibling::div[1]//*[self::h3 or self::p or self::span]/text()")
            loader.add_xpath('description', "//h2[contains(text(),'From the brand')]/following-sibling::div[1]//*[self::h3 or self::p or self::span]/text()")

            # scrape the bulleted about product features
            for feature in response.xpath("//*[@id='feature-bullets']/ul/li/span/text()").getall():
                feature = feature.strip()
                if feature:
                    loader.add_value('features', feature)

            details = {}
            for product_detail in response.xpath("//*[@id='detailBullets_feature_div']/ul/li/span[@class='a-list-item']"):
                try:
                    key = product_detail.xpath(
                        "normalize-space(.//span[@class='a-text-bold']/text())").get().replace(" \u200f : \u200e", "")
                    value = product_detail.xpath(
                        "normalize-space(.//span[@class='a-text-bold']/following-sibling::span/text())").get().replace(" \u200f : \u200e", "")
                    if "date" in key.lower():
                        try:
                            value = datetime.strptime(value, "%B %d, %Y").date().isoformat()
                        except:
                            pass
                    details[key] = value
                except:
                    pass
        
            if details == {}:
                for product_detail in response.xpath("//*[contains(@id,'productDetails')]//table/tr"):
                    try:
                        key = product_detail.xpath("normalize-space(./th/text())").get()
                        value = product_detail.xpath("normalize-space(./td/text())").get().replace("\u200e", "")
                        if "date" in key.lower():
                            try:
                                value = datetime.strptime(value, "%B %d, %Y").date().isoformat()
                            except:
                                pass

                        if "best sellers rank" in key.lower():
                            det_list = product_detail.xpath("./td/descendant::*/text()").getall()
                            value = "".join([i.strip() for i in det_list])

                        if "customer reviews" in key.lower():
                            det_list = product_detail.xpath("./td/descendant::span/text()").getall()
                            value = " ".join([i.strip() for i in det_list])

                        details[key] = value
                    except:
                        pass

            loader.add_value('details', details)

            # other category rank
            try:
                other_rank, other_cat = response.xpath("normalize-space(.//span[contains(text(),'Best Sellers Rank:')]/following-sibling::ul)").re(r"#([0-9,]+)\sin\s(.*)")
                loader.add_value("other_category_rank", other_rank)
                loader.add_value("other_category", other_cat)
            except:
                pass

            # best seller category
            try:
                rank_cat = response.xpath(".//span[contains(text(),'Best Sellers Rank:')]/following-sibling::text()").re(r"#([0-9,]+)\sin\s(.*)\s\(")
                if len(rank_cat) == 2:
                    rank, category = rank_cat
                    loader.add_value("best_seller_rank", rank)
                    loader.add_value("best_seller_category", category)
            except:
                best_seller = details.get("Best Sellers Rank")
                match = re.match("#([0-9,]+)\sin\s(.*)\s\(.*#([0-9,]+)\sin(.*)", best_seller)
                if match:
                    try:
                        br, bc, otr, otc = match.groups()
                        loader.add_value("best_seller_rank", br)
                        loader.add_value("best_seller_category", bc)
                        loader.add_value("other_category_rank", otr)
                        loader.add_value("other_category", otc)
                    except:
                        pass

            # check if reviews and questions should be scraped
            if self.settings.get("SCRAPE_QUESTIONS"):
                yield response.follow(f"https://www.amazon.com/ask/questions/asin/{asin_dict.get('asin')}", cb_kwargs={'loader': loader, 'q_count': 0}, callback=self.parse_questions, dont_filter=True)
            elif self.settings.get("SCRAPE_REVIEWS"):
                star_level = self.settings.get("REVIEW_STAR_LEVEL")
                yield response.follow(f"https://www.amazon.com/product-reviews/{asin_dict.get('asin')}/ref=acr_dp_hist_5?ie=UTF8&filterByStar={star_level}&reviewerType=all_reviews#reviews-filter-bar",
                    cb_kwargs={'loader': loader, 'r_count': 0}, callback=self.parse_reviews, dont_filter=True)
            else:
                yield loader.load_item()


    def parse_questions(self, response, loader, q_count):
        questions_limit = self.settings.get("NUM_OF_QUESIONS")
        for question in response.xpath("//div[@class='a-section askTeaserQuestions']/div"):
            if q_count == questions_limit:
                break
            question_loader = ItemLoader(item=AmazonQuestionItem(), selector=question)
            question_loader.default_output_processor = TakeFirst()
            question_loader.add_xpath('body', "normalize-space(.//a[@class='a-link-normal']/span[@data-action='ask-no-op']/text())")
            question_loader.add_xpath('answer', ".//div[span[text()='Answer:']]/following-sibling::div/span/text()")
            question_loader.add_xpath('answer', "normalize-space(.//div[span[text()='Answer:']]/following-sibling::div//span[@class='askLongText'])")
            question_loader.add_xpath("num_of_votes", ".//ul[contains(@class,'vote')]/li[@class='label']/@data-count")
            question_loader.add_value("num_of_answers", question.xpath("normalize-space(.//span[contains(text(),'See all')]/text())").re_first(r"\d+"))
            question_loader.add_xpath("answered_by", ".//span[contains(@class,'a-profile-name')]/text()")

            try:
                date = question.xpath("normalize-space(.//div[div[contains(@class,'a-profile')]]/span[last()]/text())").re_first(r"\s(.*)")
                parsed_date = datetime.strptime(date, "%B %d, %Y").date().isoformat()
                question_loader.add_value("date_answered", parsed_date)
            except:
                pass

            # check if the answer or question is in english and drop it if not
            question_text = question_loader.get_output_value("body")
            
            try:
                lang = detect(question_text)
            except:
                lang = "unknown"
            if lang != 'en':
                continue

            answer_text = question_loader.get_output_value("answer")
            try:
                lang = detect(answer_text)
            except:
                lang = "unknown"
            if lang != 'en':
                continue

            loader.add_value("questions", question_loader.load_item())
            q_count += 1

        next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/@href").get()

        if next_page_url and q_count < questions_limit:
            yield response.follow(next_page_url, cb_kwargs={'loader': loader, 'q_count': q_count}, callback=self.parse_questions, dont_filter=True)
        else:
            # scrape reviews
            if self.settings.get("SCRAPE_REVIEWS"):
                star_level = self.settings.get("REVIEW_STAR_LEVEL")
                asin = loader.get_output_value('asin')
                yield response.follow(f"https://www.amazon.com/product-reviews/{asin}/ref=acr_dp_hist_5?ie=UTF8&filterByStar={star_level}&reviewerType=all_reviews#reviews-filter-bar",
                        cb_kwargs={'loader': loader, 'r_count': 0}, callback=self.parse_reviews, dont_filter=True)
            else:
                yield loader.load_item()

    def parse_reviews(self, response, loader, r_count):
        reviews_limit = self.settings.get("NUM_OF_REVIEWS")
        for review in response.xpath("//div[@id='cm_cr-review_list']/div[@data-hook='review']"):
            if r_count == reviews_limit:
                break
            review_loader = ItemLoader(item=AmazonReviewItem(), selector=review)
            review_loader.default_output_processor = TakeFirst()
            review_loader.add_xpath('header', ".//*[@data-hook='review-title']/span/text()")
            review_loader.add_xpath('body', "normalize-space(.//*[@data-hook='review-body']//span)")
            review_loader.add_xpath('reviewer', ".//span[contains(@class,'a-profile-name')]/text()")
            review_loader.add_xpath("purchase_type", ".//span[contains(@data-hook,'avp-badge')]/text()")
            review_loader.add_value("reviewer_rating", review.xpath(".//i[contains(@data-hook,'review-star-rating')]/span/text()").re_first(r"([0-9.]+) out"))

            # get the country and date
            try:
                location, date = review.xpath(".//span[contains(@class,'review-date')]/text()").re(r"Reviewed\sin\s(.*)\son\s(.*)")
                parsed_date = datetime.strptime(date, "%B %d, %Y").date().isoformat()
                review_loader.add_value("reviewer_location", location)
                review_loader.add_value("review_date", parsed_date)
            except:
                pass

            # check if the language is english else drop it
            review_text = review_loader.get_output_value("body")
            try:
                lang = detect(review_text)
            except:
                lang = "unknown"
            if lang != 'en':
                continue

            if "United States" not in location:
                pass
            else:
                loader.add_value("reviews", review_loader.load_item())
                r_count += 1

        next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/@href").get()

        if next_page_url and r_count < reviews_limit:
            yield response.follow(next_page_url, cb_kwargs={'loader': loader, 'r_count': r_count}, callback=self.parse_reviews, dont_filter=True)
        else:
            yield loader.load_item()