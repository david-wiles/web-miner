import scrapy
import time
import socket

from scrapy.spiders import CrawlSpider, Rule
from ..items import WebItem


class DefaultCrawlSpider(CrawlSpider):
    name = "default"
    start_urls = ["https://buzzfeed.com"]

    rules = (
        Rule(follow=True, callback="parse_item"),
    )

    def parse_start_url(self, response, **kwargs):
        yield self.parse_item(response)

    def parse_item(self, response):
        yield WebItem({
            "url": response.url,
            "response": response,
            "timestamp": time.time_ns(),
            "server": socket.gethostname(),
        })
