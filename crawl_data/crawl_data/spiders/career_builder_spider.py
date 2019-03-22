import scrapy
from ..items import CareerBuilderItem
from scrapy.selector import Selector

MAX_PAGES = 20

class CareerBuilderSpider(scrapy.Spider):
    name = 'careerbuilder'

    custom_settings = {
        'crawl_data.pipelines.JsonWriterPipeline': 300
    }

    def start_requests(self):
        urls = [
            "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-vi.html",
            # "https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-trang-2-vi.html"
        ]

        for i in range(2, MAX_PAGES):
            urls.append('https://careerbuilder.vn/viec-lam/tat-ca-viec-lam-trang-{}-vi.html'.format(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # break

    def parse(self, response):
        jobs = response.xpath('//a[contains(@href, "tim-viec-lam/")]/@href').getall()
        for job in jobs:
            yield response.follow(job, self.parse_job)
            # break


    def parse_job(self, response):
        
        job_title = response.xpath('//div[@class="top-job-info"]/h1/text()').get()
        company_name = response.xpath('//div[@class="tit_company"]/text()').get()
        update_date = response.xpath('//div[@class="datepost"]/span/text()').get()
        
        end_date = response.xpath('//li[@class="bgLine2"]/p[@class="fl_right"]/text()').get()

        job_detail = self.parse_detail_job(response) 
        address = job_detail[0]
        position = job_detail[1]
        experiment_required = job_detail[2]
        salary = job_detail[3]
        categories = job_detail[4]
        end_date = job_detail[5]
        
        job_description = response.xpath('//div[@class="content_fck"]').getall()[0]
        job_requirements = response.xpath('//div[@class="content_fck"]').getall()[0]
        other_information = response.xpath('//div[@class="content_fck"]').getall()[0]

        company_address = response.xpath('//p[@class="TitleDetailNew"]/label/label/text()').get()
        try:
            company_size = response.xpath('//div[@class="LeftJobCB"]/text()').re('\w*-\w*')[0]
        except Exception:
            company_size = ''

        item = CareerBuilderItem(
            job_title=job_title,
            job_description=job_description,
            company_name=company_name,
            update_date=update_date,
            end_date=end_date,
            address=address,
            salary=salary,
            categories=categories,
            position=position,
            job_requirements=job_requirements,
            other_information=other_information,
            company_address=company_address,
            experiment_required=experiment_required,
            company_size=company_size
        )
        yield item

    def parse_detail_job(self, response):
        detail_job_new = response.xpath('//ul[@class="DetailJobNew"]/li/p')
        address = ''
        position = ''
        experiment_required = ''
        salary = ''
        categories = ''
        end_date = ''
        for field in detail_job_new:
            key = field.xpath('span/text()').get()
            # print(key)
            if key == 'Nơi làm việc: ':
                address = field.xpath('b/a/text()').get()
            elif key == 'Cấp bậc: ':
                position = field.xpath('label/text()').get()
            elif key == 'Kinh nghiệm: ':
                experiment_required = field.xpath('text()').get().strip()
            elif key == 'Lương: ':
                salary = field.xpath('label/text()').getall()
            elif key == 'Ngành nghề: ':
                categories = field.xpath('b/a/text()').getall()
            elif key == 'Hết hạn nộp: ':
                end_date = field.xpath('text()').get()

        return (address, position, experiment_required, salary, categories, end_date)
        
