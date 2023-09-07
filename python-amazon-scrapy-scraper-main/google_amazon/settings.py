from itertools import cycle
from datetime import datetime
import pathlib
import logging

BOT_NAME = 'google_amazon'

SPIDER_MODULES = ['google_amazon.spiders']
NEWSPIDER_MODULE = 'google_amazon.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Set number of parallel requests
CONCURRENT_REQUESTS = 50

# smart proxy credentials
SMARTPROXY_USER = 'sp96556092'
SMARTPROXY_PASSWORD = 'trs#658lTh'

# uncomment the ones you need to use either eu or us proxies
# US proxies
# SMARTPROXY_ENDPOINT = 'gate.dc.smartproxy.com'
# SMARTPROXY_PORTS = cycle([i for i in range(20001,37960)])
# EU proxies
SMARTPROXY_ENDPOINT = 'eu.dc.smartproxy.com' 
SMARTPROXY_PORTS = cycle([i for i in range(20001,29980)])
# all countries proxies
# SMARTPROXY_ENDPOINT = 'all.dc.smartproxy.com' 
# SMARTPROXY_PORTS = cycle([i for i in range(10001,49999)])


# rotating user agents
RANDOM_UA_TYPE = 'desktop'
logging.getLogger('scrapy_user_agents.user_agent_picker').setLevel('CRITICAL') # disable excess log output

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400, # comment if you do not want rotating user agents
}

# Zyte smart proxy 
ZYTE_SMARTPROXY_ENABLED = True
ZYTE_SMARTPROXY_APIKEY = '455fe7d72d1c433b99cb2cf35bb839d4'

# increase retries in case proxies fail
RETRY_TIMES = 20

# image downloading and saving
IMAGES_STORE = "images"
ITEM_PIPELINES = {
    # 'google_amazon.pipelines.MongoDBPipeline': 295,
    # 'google_amazon.pipelines.PostgresDBPipeline': 300,
}

# postgres database connection settings
DATABASE_HOST = 'localhost'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'
DATABASE_PORT = '5432'
DATABASE_NAME = 'google_amazon'

# mongodb connection settings
MONGO_URI = 'mongodb://localhost:27017' # or with aunthentication 'mongodb://username:password@localhost:27017'
MONGO_DATABASE = 'google_amazon'

# scrape reviews
SCRAPE_REVIEWS = True
NUM_OF_REVIEWS = 25
REVIEW_STAR_LEVEL = 'five_star' # can be any of 'five_star', four_star', 'three_star', 'two_star', 'one_star' or 'all_star'

# scrape questions
SCRAPE_QUESTIONS = True
NUM_OF_QUESIONS = 25

# uncomment if you want to save output to csv file
# file will be compressed with gzip to save on space
FEEDS = {
    pathlib.Path(f"scraped_data/scraped_items_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.csv.gz"): {
        "format": "csv",
        "overwrite": True,
        'postprocessing': ['scrapy.extensions.postprocessing.GzipPlugin'],
        'gzip_compresslevel': 5,
    }
}

# Increase download timeout for image downloads
DOWNLOAD_TIMEOUT = 1200 # 20 minutes
MEDIA_ALLOW_REDIRECTS = True

# use log file for debugging and set logging level to warning
# LOG_FILE = "data.log"
# LOG_LEVEL = logging.WARNING