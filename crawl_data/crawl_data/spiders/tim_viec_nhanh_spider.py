import scrapy
from ..items import TimViecNhanhItem


class TimViecNhanhSpider(scrapy.Spider):
    name = "timviecnhanh"

    root_url = 'www.timviecnhanh.com'

    custom_settings = {
        'crawl_data.pipelines.JsonWriterPipeline': 300
    }

    def start_requests(self):
        urls = [
            "https://www.timviecnhanh.com/viec-lam-kinh-doanh-c32.html",
            "https://www.timviecnhanh.com/viec-lam-hanh-chinh-thu-ky-tro-ly-c29.html",
            "https://www.timviecnhanh.com/viec-lam-cham-soc-khach-hang-c21.html",
            "https://www.timviecnhanh.com/viec-lam-sinh-vien-moi-tot-nghiep-thuc-tap-c35.html",
            "https://www.timviecnhanh.com/viec-lam-dien-dien-tu-dien-lanh-c22.html",
            "https://www.timviecnhanh.com/viec-lam-quang-cao-marketing-pr-c45.html",
            "https://www.timviecnhanh.com/viec-lam-phat-trien-thi-truong-c65.html",
            "https://www.timviecnhanh.com/viec-lam-cong-nghe-thong-tin-c17.html",
            "https://www.timviecnhanh.com/viec-lam-thiet-ke-my-thuat-c49.html",
            "https://www.timviecnhanh.com/viec-lam-kien-truc-noi-that-c31.html",
            "https://www.timviecnhanh.com/viec-lam-nhan-su-c40.html",
            "https://www.timviecnhanh.com/viec-lam-duoc-hoa-chat-sinh-hoa-c24.html",
            "https://www.timviecnhanh.com/viec-lam-ngoai-ngu-c56.html",
            "https://www.timviecnhanh.com/viec-lam-xuat-nhap-khau-ngoai-thuong-c53.html",
            "https://www.timviecnhanh.com/viec-lam-bien-dich-phien-dich-c14.html",
            "https://www.timviecnhanh.com/viec-lam-y-te-c54.html",
            "https://www.timviecnhanh.com/viec-lam-det-may-c19.html",
            "https://www.timviecnhanh.com/viec-lam-phuc-vu-tap-vu-giup-viec-c66.html",
            "https://www.timviecnhanh.com/viec-lam-lam-dep-the-luc-spa-c59.html",
            "https://www.timviecnhanh.com/viec-lam-moi-truong-xu-ly-chat-thai-c36.html",
            "https://www.timviecnhanh.com/viec-lam-bao-chi-bien-tap-vien-c12.html",
            "https://www.timviecnhanh.com/viec-lam-khac-c55.html",
            "https://www.timviecnhanh.com/viec-lam-quan-he-doi-ngoai-c42.html",
            "https://www.timviecnhanh.com/viec-lam-luat-phap-ly-c34.html",
            "https://www.timviecnhanh.com/viec-lam-trang-thiet-bi-cong-nghiep-c61.html",
            "https://www.timviecnhanh.com/viec-lam-dau-khi-dia-chat-c18.html",
            "https://www.timviecnhanh.com/viec-lam-trang-thiet-bi-van-phong-c63.html",
            "https://www.timviecnhanh.com/viec-lam-trang-thiet-bi-gia-dung-c62.html",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath('//a[contains(@class,"item")]/@href').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        next_page_url = response.xpath('//a[@class="next item"]/@href').get()
        for url in next_page_url:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse(self, response):
        job_title = response.xpath('//header[@class="block-title"]/h1/span/text()').get().strip()
        link_job = response.url
        company_name = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/h3/a/text()').extract()[0].strip()
        company_address = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/h3/a/text()').extract()[0].strip()
        company_website = response.xpath('//div[@class="col-xs-6 p-r-10 offset10"]/h3/a/@href').extract()[0]
        time_update = response.xpath('//div[@class="col-xs-3 offset10"]/time/text()').extract()[0].strip()
        level_solary = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul[@class="no-style"]/li[1]/text()').extract()[1].strip()
        requied_experience = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[2]/text()').extract()[1].strip()
        degree = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[3]/text()').extract()[1].strip()
        provincial = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[4]/a/text()').extract()[0].strip()
        career_arr = response.xpath('//div[@class="col-xs-4 offset20 push-right-20"]/ul/li[5]/a/text()').extract()
        career = ""
        for x in career_arr:
            career +=x +", "
        #
        number_of_recruitment = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[1]/text()').extract()[1].strip()
        genrder_required = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[2]/text()').extract()[1].strip()
        nature_of_work = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[3]/text()').extract()[1].strip()
        work_form = response.xpath('//div[@class="col-xs-4 offset20"]/ul/li[4]/text()').extract()[1].strip()
        #
        dealine_for_submit = response.xpath('//table/tbody/tr[4]/td[2]/b/text()').extract()[0].strip()
        job_description_arr = response.xpath('//table/tbody/tr[1]/td[2]/p/text()').extract()
        job_description = ""
        for x in job_description_arr:
            job_description += x + "\n"
        requirement_arr = response.xpath('//table/tbody/tr[2]/td[2]/p/text()').extract()
        requirement = ""
        for x in requirement_arr:
            requirement += x + "\n"
        job_benefit = response.xpath('//table/tbody/tr[3]/td[2]/p/text()').extract()

        item = TimViecNhanhItem(
            job_title = job_title,
            link_job = link_job,
            company_name = company_name,
            company_address = company_address,
            company_website = company_website,
            time_update = time_update,
            level_solary = level_solary,
            requied_experience = requied_experience,
            degree = degree,
            provincial = provincial,
            career =career,
            number_of_recruitment = number_of_recruitment,
            genrder_required = genrder_required,
            nature_of_work = nature_of_work,
            work_form = work_form,
            dealine_for_submit = dealine_for_submit,
            job_description = job_description,
            requirement = requirement,
            job_benefit = job_benefit

        )
        if item['job_title']:
            yield item