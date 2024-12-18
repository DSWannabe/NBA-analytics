# Scrapy settings for NBA project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import re
import os

BOT_NAME = "NBA"

SPIDER_MODULES = ["NBA.spiders"]
NEWSPIDER_MODULE = "NBA.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = True

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = False
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Playwright

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 60 * 1000,  # Increased to 60 seconds
}

# settings.py

# Enable the Scrapy Playwright middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_playwright.middleware.ScrapyPlaywrightDownloadHandler': 543,
}

# Define the Playwright browser types to be launched
PLAYWRIGHT_BROWSER_TYPE = 'chromium'


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "NBA.middlewares.NbaSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "NBA.middlewares.NbaDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "NBA.pipelines.GameStatsPipeline": 300,
    # "NBA.pipelines.SeasonalStatsPipeline": 301,
    # "NBA.pipelines.PlayerUrlsPipeline": 302,
    # "NBA.pipelines.PlayerInfoPipeline": 303,
    # "NBA.pipelines.PlayerInfoPipeline2": 304,
}

NBA_PIPELINE_OUTPUT_FOLDER = os.path.expanduser("./data")
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

def should_abort_request(request):
    """Intercept all requests and abort blocked ones."""
    # if request.resource_type in [
    #     "beacon",
    #     "csp_report",
    #     "font",
    #     "imageset",
    #     "media",
    #     "object",
    #     "texttrack",
    #     "image",
    #     # 'stylesheet',
    #     # 'script',
    #     # 'xhr',
    # ]:
    #     return True
    if re.findall(r"(\.png$)|(\.jpg$)|(\.gif$)", request.url, re.IGNORECASE):
        return True
    return False


PLAYWRIGHT_ABORT_REQUEST = should_abort_request
