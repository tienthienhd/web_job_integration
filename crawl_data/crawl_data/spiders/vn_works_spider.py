import scrapy
# from ..items import JobItem
from scrapy.selector import Selector


class VNWorksSpider(scrapy.Spider):
    name = 'vietnamworks'

    def start_requests(self):
        urls = [
            "https://www.vietnamworks.com/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass


    def parse_job(self, response):
        pass