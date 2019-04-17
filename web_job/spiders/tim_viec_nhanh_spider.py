import scrapy
from ..items import TimViecNhanhItem


class TimViecNhanhSpider(scrapy.Spider):
    name = "timviecnhanh"

    root_url = 'www.timviecnhanh.com'

    custom_settings = {
        'crawl_data.pipelines.JsonWriterPipeline': 300,
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        urls = [
            'https://www.timviecnhanh.com'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_categories)

    def parse_categories(self, response):
        categories = response.xpath('//div[@id="field-hot-content"]/ul/li/a/@href').getall()
        for category in categories:
            yield scrapy.Request(url=category, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath('//a[contains(@class,"item")]/@href').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        next_page_url = response.xpath('//a[contains(@class,"next item")]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse(self, response):
        job_title = response.xpath('//header[@class="block-title"]/h1/span/text()').get()
        update_date = response.xpath('//time[@class="entry-date published"]/text()').get()
        address = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul[@class="no-style"]/li[4]/a/text()').getall()

        company_name = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/h3/a/text()').get().strip()
        company_address = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/span/text()').get()[9:]
        # company_website = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/h3/a/@href').extract()[0]
        # time_update = response.xpath('//div[@class="col-xs-3 offset10"]/time/text()').extract()[0].strip()
        salary = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul[@class="no-style"]/li[1]/text()').getall()[1].strip()
        requied_experience = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[2]/text()').getall()[1].strip()
        degree = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[3]/text()').getall()[1].strip()
        # provincial = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[4]/a/text()').extract()[0].strip()
        categories = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[5]/a/text()').getall()

        number_of_recruitment = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[1]/text()').getall()[1].strip()
        sex = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[2]/text()').getall()[1].strip()
        nature_of_work = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[3]/text()').getall()[1].strip()
        work_form = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[4]/text()').extract()[1].strip()
        #

        dealine_for_submit = response.xpath('//table/tbody/tr[4]/td[2]/b/text()').get().strip()
        job_description_arr = response.xpath('//table/tbody/tr[1]/td[2]/p/text()').getall()
        job_description = ""
        for x in job_description_arr:
            job_description += x.strip() + "\n"
        requirement_arr = response.xpath('//table/tbody/tr[2]/td[2]/p/text()').getall()
        requirement = ""
        for x in requirement_arr:
            requirement += x.strip() + "\n"
        benefits = ""
        job_benefit = response.xpath('//table/tbody/tr[3]/td[2]/p/text()').getall()
        for x in job_benefit:
            benefits += x.strip() + '\n'

        item = TimViecNhanhItem(
            job_title=job_title,
            address=address,
            company_name=company_name,
            company_address=company_address,
            update_date=update_date,
            salary=salary,
            requied_experience=requied_experience,
            degree=degree,
            categories=categories,
            number_of_recruitment=number_of_recruitment,
            sex=sex,
            nature_of_work=nature_of_work,
            work_form=work_form,
            dealine_for_submit=dealine_for_submit,
            job_description=job_description,
            requirement=requirement,
            benefits=benefits
        )
        if item['job_title']:
            yield item