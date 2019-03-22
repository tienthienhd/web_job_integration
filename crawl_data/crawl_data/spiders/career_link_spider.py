import scrapy
from ..items import CareerLinkItem


class CareerLinkSpider(scrapy.Spider):
    name = "careerlink"
    MAX_PAGE_PER_LOC = 20

    root_url = 'https://www.careerlink.vn'

    custom_settings = {
        'crawl_data.pipelines.JsonWriterPipeline': 300
    }

    def start_requests(self):
        urls = [
            'https://www.careerlink.vn/tim-viec-lam-nhanh'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        locations = response.xpath('//a[contains(@title, "View All Jobs at Location")]/@href').getall()
        for location in locations:
            url_location = self.root_url + location
            yield scrapy.Request(url=url_location, callback=self.parse_location)
            # break
    
    def parse_location(self, response):
        url_locations = []
        for i in range(1, self.MAX_PAGE_PER_LOC):
            url_locations.append(response.url + "?view=headline&page={}".format(i))
            
        for url in url_locations:
            yield scrapy.Request(url=url, callback=self.parse_jobs)
            # break
    
    def parse_jobs(self, response):
        url_jobs = response.xpath('//a[@target="_blank" and contains(@href, "/tim-viec-lam")]/@href').getall()
        for url in url_jobs:
            url = self.root_url + url
            yield scrapy.Request(url=url, callback=self.parse_job)
            # break

    def parse_job(self, response):
        job_title = response.xpath('//h1/span[@itemprop="title"]/text()').get().strip()
        street_address = response.xpath('//span[@itemprop="streetAddress"]/text()').get().strip()
        address_locality = response.xpath('//span[@itemprop="addressLocality"]/text()').get().strip()
        address_region = response.xpath('//span[@itemprop="addressRegion"]/text()').get().strip()
        address_country = response.xpath('//span[@itemprop="addressCountry"]/text()').get().strip()
        
        salary = response.xpath('//span[@itemprop="baseSalary"]/*[not(@class="hidden")]/text()').getall()

        job_description = response.xpath('//div[@itemprop="description"]').get()
        skills = response.xpath('//div[@itemprop="skills"]').getall()

        categories, position, education_requirements, experience_requirements, employment_type, sex = self.get_job_detail(response)

        dates = response.xpath('//dl/*/text()').getall()
        begin_date = dates[1].strip()
        end_date = dates[4].strip()

        company_name = response.xpath('//dt[@class="company-name"]/a/span/span[@itemprop="name"]/text()').get().strip()
        company_size = response.xpath('//span[@itemprop="numberOfEmployees"]/text()').get().strip()

        item = CareerLinkItem(
            job_title=job_title,
            street_address=street_address,
            address_locality=address_locality,
            address_region=address_region,
            address_country=address_country,
            salary=salary,
            job_description=job_description,
            skills=skills,
            categories=categories,
            position=position,
            education_requirements=education_requirements,
            experience_requirements=experience_requirements,
            employment_type=employment_type,
            sex=sex,
            begin_date=begin_date,
            end_date=end_date,
            company_name=company_name,
            company_size=company_size
        )

        yield item

    def get_job_detail(self, response):
        details = response.xpath('//ul[@class="list-unstyled"]/li')
        for field in details:
            key = field.xpath('text()').get().strip()
            if key.startswith('Mã việc làm:'):
                pass
            elif key.startswith('Ngành nghề việc làm:'):
                categories = response.xpath('//span[@itemprop="occupationalCategory"]/text()').getall()
                for i, value in enumerate(categories):
                    categories[i] = value.strip()
            elif key.startswith('Cấp bậc:'):
                position = key.split(':')[-1].strip()
            elif key.startswith('Nơi làm việc:'):
                pass 
            elif key.startswith('Trình độ học vấn:'):
                education_requirements = response.xpath('//span[@itemprop="educationRequirements"]/text()').get().strip()
            elif key.startswith('Mức kinh nghiệm:'):
                experience_requirements = response.xpath('//span[@itemprop="experienceRequirements"]/text()').get().strip()
            elif key.startswith('Loại công việc:'):
                employment_type = response.xpath('//span[@itemprop="employmentType"]/text()').get().strip()
            elif key.startswith('Giới tính:'):
                sex = key.split(':')[-1].strip()
            elif key.startswith('Cách liên hệ:'):
                pass 
            elif key.startswith('Tên liên hệ:'):
                pass 
            elif key.startswith('Địa chỉ:'):
                pass
            elif key.startswith('Email liên hệ:'):
                pass 
            elif key.startswith('Điện thoại liên lạc:'):
                pass 
        return categories, position, education_requirements, experience_requirements, employment_type, sex

        


