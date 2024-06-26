# Scrapy settings for temporary_scaper_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from dotenv import load_dotenv
import os
from logging.config import dictConfig
load_dotenv(".env")

BOT_NAME = "temporary_scaper_spider"

SPIDER_MODULES = ["temporary_scaper_spider.spiders"]
NEWSPIDER_MODULE = "temporary_scaper_spider.spiders"


LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/scrapy.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
            'formatter': 'standard',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'formatter': 'standard',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['info_file', 'error_file', 'debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scrapy': {
            'handlers': ['info_file', 'error_file', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

dictConfig(LOGGING)


SCRAPEOPS_API_KEY = str(os.getenv('API-KEY'))
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = ''
# FEEDS = {
#     'booksdata.json': {'format': 'json'}
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "temporary_scaper_spider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "temporary_scaper_spider.middlewares.TemporaryScaperSpiderSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "temporary_scaper_spider.middlewares.FakeHTTPHeaderMiddleware": 400,
    # "rotating_proxies.middlewares.RotatingProxyMiddleware":610,
    # "rotating_proxies.middlewares.BanDetectionMiddleware":620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "temporary_scaper_spider.pipelines.BookScraperPipeline": 300,
    "temporary_scaper_spider.pipelines.SQLAlchemyPipeline": 400,
    # "temporary_scaper_spider.pipelines.MYSQLPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ROTATING_PROXY_LIST_PATH = 'proxies.txt'

NUM_OF_RESULTS = 50