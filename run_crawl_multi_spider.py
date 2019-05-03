import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from web_job.spiders.career_builder_spider import CareerBuilderSpider
from web_job.spiders.career_link_spider import CareerLinkSpider
from web_job.spiders.tim_viec_nhanh_spider import TimViecNhanhSpider


configure_logging()
runner = CrawlerRunner(get_project_settings())
runner.crawl(CareerBuilderSpider)
runner.crawl(CareerLinkSpider)
runner.crawl(TimViecNhanhSpider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
