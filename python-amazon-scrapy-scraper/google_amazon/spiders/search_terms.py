import scrapy
from urllib.parse import urlencode
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader
from google_amazon.items import SearchResultItem
import pandas as pd
from scrapy.downloadermiddlewares.retry import get_retry_request
import re
import json
from datetime import datetime

class SearchTermSpider(scrapy.Spider):
    name = 'search_terms'
    allowed_domains = ['google.com', 'amazon.com', 'media-amazon.com']
    scraping_date = datetime.now().strftime("%Y-%m-%d") # used to create a folder for the date to store files

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'google_amazon.pipelines.AmazonImagesPipeline': 1,
            'google_amazon.pipelines.PerFilenameExportPipeline': 305,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'google_amazon.middlewares.SmartProxyMiddleware': 100,
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
        }
    }

    def __init__(self, file_name="keywords.csv"):
        self.file_name = file_name

    def start_requests(self):
        data = pd.read_csv(self.file_name)
        for row in data.itertuples():
            qs = {'q': f"{row.Keyword} amazon"}
            qs = urlencode(qs)
            yield scrapy.Request(f"https://google.com/search?{qs}", cb_kwargs={"search_term": row})
            # search amazon
            qs = {'k': f"{row.Keyword}"}
            qs = urlencode(qs)
            yield scrapy.Request(f"https://www.amazon.com/s?{qs}", callback=self.parse_amazon, cb_kwargs={'search_term': row})

    def parse(self, response, search_term):
        # extract amazon links and follow them
        urls = response.xpath("//a[h3]/@href").re(r"https:\/\/www\.amazon\.com.*")
        
        for url in urls:
            yield response.follow(url, callback=self.parse_amazon, cb_kwargs={"search_term": search_term})
    

    def parse_amazon(self, response, search_term): 
        # check if response is empty and retry
        if not response.text:
            new_request_or_none = get_retry_request(
                response.request,
                spider=self,
                reason='Response is empty',
                max_retry_times=100
            )
            new_request_or_none.dont_filter = True
            yield new_request_or_none 
        else:
            # loop through the results and yield the response
            for result in response.xpath("//*[@data-component-type='s-search-result']"):
                l = ItemLoader(item=SearchResultItem(), response=response, selector=result)
                l.default_output_processor = TakeFirst()

                url = result.xpath(".//h2/a/@href").re_first(r"(.*)\/ref.*")
                if url is not None and not "/gp/slredirect" in url:
                    # populate the item and yield it
                    l.add_value("search_term_id", search_term.ID)
                    l.add_value("search_term", search_term.Keyword)
                    l.add_xpath("name", ".//h2/a/span/text()")
                    l.add_xpath("asin", "./@data-asin")
                    l.add_value("url", response.urljoin(url))
                    l.add_value("amazon_search_url", response.url)
                    l.add_value("star_rating", result.xpath(".//span[contains(@aria-label,'out of 5 stars')]/@aria-label").re_first(r"([0-9\.]+)\sout"))
                    l.add_xpath("num_of_ratings", ".//span[contains(@aria-label,'out of 5 stars')]/following-sibling::span/@aria-label")
                    # price whole and fraction parts
                    l.add_xpath("price", "normalize-space(.//span[@class='a-price-whole']/text())")
                    l.add_xpath("price", "normalize-space(.//span[@class='a-price-fraction']/text())")

                    l.add_xpath("currency", ".//span[@class='a-price-symbol']/text()")
                    l.add_xpath("discount_pct", ".//span[@class='a-price']/preceding-sibling::span/text()")
                    l.add_xpath("image_urls", "(.//img[@class='s-image'])[1]/@src")
                    yield l.load_item()

            # scrape the next pages
            next_page = response.xpath("//a[contains(@class,'s-pagination-next')]/@href")
            if next_page.re_first(r"page=(\d+)") in ['2', '3']:
                self.logger.info("scraping next pages")
                yield response.follow(next_page.get(), callback=self.parse_amazon, cb_kwargs={"search_term": search_term})

        # if its an asin page scrape the results
        if re.match(r".*/dp/.*", response.url):
            l = ItemLoader(item=SearchResultItem(), response=response)
            l.default_output_processor = TakeFirst()
            # populate the item and yield it
            l.add_value("search_term_id", search_term.ID)
            l.add_value("search_term", search_term.Keyword)
            l.add_xpath("name", "normalize-space(//*[@id='productTitle']/text())")
            l.add_xpath("asin", "//*/@data-asin")
            l.add_xpath("url", "//link[@rel='canonical']/@href")
            l.add_value("amazon_search_url", response.url)
            l.add_value("star_rating", response.xpath("//span[@id='acrPopover']/@title").re_first(r"([0-9\.]+)\sout"))
            l.add_value("num_of_ratings", response.xpath("//span[@id='acrCustomerReviewText']/text()").re_first(r"([0-9\.,]+)\sratings"))
            # price whole and fraction parts
            l.add_xpath("price", "normalize-space(//span[@class='a-price-whole']/text())")
            l.add_xpath("price", "normalize-space(//span[@class='a-price-fraction']/text())")

            l.add_xpath("currency", "//span[@class='a-price-symbol']/text()")
            l.add_xpath("discount_pct", "//span[contains(@class,'savingsPercentage')]/text()")

            # scrape images
            images = response.xpath("//script/text()").re_first(r"'initial':\s+(\[.*\])")
            images_parsed = json.loads(images)
            # loader.add_xpath('image_urls', "//*[@class='a-button-text']/img[contains(@src,'m.media-amazon.com')]/@src")
            for img in images_parsed:
                l.add_value("image_urls", img.get('hiRes'))
            yield l.load_item()