# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class JobItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     job_title = scrapy.Field()
#     job_description = scrapy.Field()
#     job_requirements = scrapy.Field()
#     categories = scrapy.Field()
#     experiment_required = scrapy.Field()
#     degree_required = scrapy.Field()
#     employment_type = scrapy.Field()
#     num_views = scrapy.Field()
#     begin_date = scrapy.Field()
#     end_date = scrapy.Field()
#     update_date = scrapy.Field()
#     min_salary = scrapy.Field()
#     max_salary = scrapy.Field()

#     company = scrapy.Field()

class CareerBuilderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    job_description = scrapy.Field()
    job_requirements = scrapy.Field()
    address = scrapy.Field()
    categories = scrapy.Field()
    end_date = scrapy.Field()
    update_date = scrapy.Field()
    salary = scrapy.Field()
    position = scrapy.Field()
    other_information = scrapy.Field()
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    company_size = scrapy.Field()
    experiment_required = scrapy.Field()


class CareerLinkItem(scrapy.Item):
    job_title = scrapy.Field()
    street_address = scrapy.Field()
    address_locality = scrapy.Field()
    address_region = scrapy.Field()
    address_country = scrapy.Field()
    salary = scrapy.Field()
    job_description = scrapy.Field()
    skills = scrapy.Field()
    categories = scrapy.Field()
    position = scrapy.Field()
    education_requirements = scrapy.Field()
    experience_requirements = scrapy.Field()
    employment_type = scrapy.Field()
    sex = scrapy.Field()
    begin_date = scrapy.Field()
    end_date = scrapy.Field()
    company_name = scrapy.Field()
    company_size = scrapy.Field()


class TimViecNhanhItem(scrapy.Item):
    id = scrapy.Field()
    job_title = scrapy.Field()
    link_job = scrapy.Field()
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    company_website = scrapy.Field()
    time_update = scrapy.Field()
    level_solary = scrapy.Field()
    requied_experience = scrapy.Field()
    degree = scrapy.Field()
    provincial = scrapy.Field()
    career = scrapy.Field()
    number_of_recruitment = scrapy.Field()
    genrder_required = scrapy.Field()
    nature_of_work = scrapy.Field()
    work_form = scrapy.Field()
    dealine_for_submit = scrapy.Field()
    job_description = scrapy.Field()
    requirement = scrapy.Field()
    job_benefit = scrapy.Field()