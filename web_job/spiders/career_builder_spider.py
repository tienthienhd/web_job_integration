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
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # break

    def parse(self, response):
        jobs = response.xpath('//a[contains(@href, "tim-viec-lam/")]/@href').getall()
        for job in jobs:
            yield response.follow(job, self.parse_job)

        next_page = response.xpath('//div[@class="paginationTwoStatus"]/a[@class="right"]/@href').get()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_job(self, response):

        job_title = response.xpath('//div[@class="top-job-info"]/h1/text()').get()
        company_name = response.xpath('//div[@class="tit_company"]/text()').get()
        update_date = response.xpath('//div[@class="datepost"]/span/text()').get()

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
                for i, category in enumerate(categories):
                    if category.endswith(','):
                        categories[i] = category[:-1]
            elif key == 'Hết hạn nộp: ':
                end_date = field.xpath('text()').get().strip()

        benefits = response.xpath('//ul[@class="list-benefits"]/li/text()').getall()
        job_description = response.xpath('//div[@class="content_fck"]').getall()[0]

        job_requirements = response.xpath('//div[@class="content_fck"]').getall()[1]

        diploma = ''
        age = ''
        sex = ''
        job_type = ''
        time_trail_work = ''
        time_work = ''
        other_information = response.xpath('//div[@class="content_fck"]')[2]
        for f in other_information.xpath('ul/li/text()').getall():
            f = f.strip()
            a = f.split(':')
            if len(a) < 2:
                continue
            a[0] = a[0].strip()
            a[1] = a[1].strip()
            if a[0] == 'Bằng cấp':
                diploma = a[1]
            elif a[0] == 'Độ tuổi':
                age = a[1]
            elif a[0] == 'Giới tính':
                sex = a[1]
            elif a[0] == 'Hình thức':
                job_type = a[1]
            elif a[0] == 'Thời gian thử việc':
                time_trail_work = a[1]
            elif a[0] == 'Thời gian làm việc':
                time_work = a[1]

        company_address = response.xpath('//p[@class="TitleDetailNew"]/label/label/text()').get().strip()
        company_size = ''
        tmp = response.xpath('//div[@class="LeftJobCB"]/text()').getall()
        for t in tmp:
            t = t.strip()
            if t.startswith('Qui mô công ty:'):
                s = t.split(':')
                company_size = s[1].strip()
                break

        item = CareerBuilderItem(
            job_title=job_title,
            company_name=company_name,
            update_date=update_date,
            address=address,
            position=position,
            experiment_required=experiment_required,
            salary=salary,
            categories=categories,
            end_date=end_date,
            benefits=benefits,
            job_description=job_description,
            job_requirements=job_requirements,
            diploma=diploma,
            age=age,
            sex=sex,
            job_type=job_type,
            time_trail_work=time_trail_work,
            time_work=time_work,
            company_address=company_address,
            company_size=company_size
        )
        yield item

