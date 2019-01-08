# -*- coding: utf-8 -*-

# Scrapy settings for Zhenai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Zhenai'

SPIDER_MODULES = ['Zhenai.spiders']
NEWSPIDER_MODULE = 'Zhenai.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Zhenai (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    "Cookie":"dgpw=1; isFirstLoadPage=1; login_health=2efb72bd87241c9ef57fed5cac4216cb4bbfa9e19f1ad193a4f348e34eba0e341e774756b584355747a1c1bff14dd76561a450cec05c9d5636bcb23c2f8655fb; token=110582440.1543297280032.458ca703f891b8a9fa46749035def78b; p=%5E%7Eworkcity%3D10101204%5E%7Esex%3D0%5E%7Emt%3D1%5E%7Enickname%3D%E7%AD%89%E4%B8%80%E4%B8%AA%E4%BD%A0%5E%7Edby%3D6a6131d467aa4b%5E%7Elh%3D110582440%5E%7Eage%3D30%5E%7E; isSignOut=%5E%7ElastLoginActionTime%3D1543297280033%5E%7E; mid=%5E%7Emid%3D110582440%5E%7E; loginactiontime=%5E%7Eloginactiontime%3D1543297280033%5E%7E; logininfo=%5E%7Elogininfo%3D110582440%5E%7E; live800=%5E%7EinfoValue%3DuserId%253D110582440%2526name%253D110582440%2526memo%253D%5E%7E; preLG_110582440=2018-11-27+08%3A52%3A45; _pc_login_isWeakPwd=1; sid=sSjMXJtoO5HJ9yuT9TNO; validate_110582440=yes; smail_110582440=yes; JSESSIONID=abcq_rOit5G4Wa3jaStDw; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1541998424,1543297307; zxr_index_110582440=1; Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2=1543300813; clientp=31242",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",


}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Zhenai.middlewares.ZhenaiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Zhenai.middlewares.ZhenaiDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Zhenai.pipelines.ZhenaiPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
