# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from .items import MediatedItem
from scrapy.exceptions import DropItem
from similarity.normalized_levenshtein import NormalizedLevenshtein
from similarity.jarowinkler import JaroWinkler
from similarity.jaccard import Jaccard


class WebJobPipeline(object):

    def process_item(self, item, spider):
        return item


class MappingPipeline(object):

    def __init__(self):
        file = 'schema_mapping/schema_mapping'
        mappings = {}
        key = None
        fields = []
        with open(file, 'r') as f:
            while True:
                line = f.readline()
                line = line[:-1]
                if line == '':
                    if len(fields) > 0:
                        mappings[key] = fields
                        fields = []
                    break

                if line.startswith('#'):
                    if len(fields) > 0:
                        mappings[key] = fields
                        fields = []
                    key = line[1:]
                else:
                    line = line.split(':')
                    if '+' in line[1]:
                        line[1] = line[1].split('+')

                    fields.append(line)

        self.mapping = mappings
        self.idx = 0

    def process_item(self, item, spider):
        target = {}
        for field in self.mapping[item['source']]:
            if field[0] == 'source':
                target[field[0]] = field[1]
                continue
            if type(field[1]) is list:
                target[field[0]] = self.add_fields(item, field[1])
            elif field[1] == '':
                target[field[0]] = ''
            else:
                target[field[0]] = item[field[1]]

        mediated_item = MediatedItem(
            idx=self.idx,
            job_title=target['job_title'],
            address=target['address'],
            job_description=target['job_description'],
            categories=target['categories'],
            update_date=target['update_date'],
            end_date=target['end_date'],
            salary=target['salary'],  # xử lý khi cho vào mongodb
            position=target['position'],
            age=target['age'],
            sex=target['sex'],
            benefits=target['benefits'],
            experiment_required=target['experiment_required'],
            diploma=target['diploma'],
            company_name=target['company_name'],
            company_address=target['company_address'],
            company_size=target['company_size'],
            source=target['source']
        )
        self.idx += 1
        return mediated_item

    @staticmethod
    def add_fields(item, fields):
        results = ""
        for field in fields:
            results += str(item[field]) + ', '

        return results


class NormalizeAddressPipeline(object):
    provinces = {"An Giang",
                 "Bà Rịa - Vũng Tàu",
                 "Bắc Giang",
                 "Bắc Kạn",
                 "Bạc Liêu",
                 "Bắc Ninh",
                 "Bến Tre",
                 "Bình Định",
                 "Bình Dương",
                 "Bình Phước",
                 "Bình Thuận",
                 "Cà Mau",
                 "Cao Bằng",
                 "Đắk Lắk",
                 "Đắk Nông",
                 "Điện Biên",
                 "Đồng Nai",
                 "Đồng Tháp",
                 "Gia Lai",
                 "Hà Giang",
                 "Hà Nam",
                 "Hà Tĩnh",
                 "Hải Dương",
                 "Hậu Giang",
                 "Hòa Bình",
                 "Hưng Yên",
                 "Khánh Hòa",
                 "Kiên Giang",
                 "Kon Tum",
                 "Lai Châu",
                 "Lâm Đồng",
                 "Lạng Sơn",
                 "Lào Cai",
                 "Long An",
                 "Nam Định",
                 "Nghệ An",
                 "Ninh Bình",
                 "Ninh Thuận",
                 "Phú Thọ",
                 "Quảng Bình",
                 "Quảng Nam",
                 "Quảng Ngãi",
                 "Quảng Ninh",
                 "Quảng Trị",
                 "Sóc Trăng",
                 "Sơn La",
                 "Tây Ninh",
                 "Thái Bình",
                 "Thái Nguyên",
                 "Thanh Hóa",
                 "Thừa Thiên Huế",
                 "Tiền Giang",
                 "Trà Vinh",
                 "Tuyên Quang",
                 "Vĩnh Long",
                 "Vĩnh Phúc",
                 "Yên Bái",
                 "Phú Yên",
                 "Cần Thơ",
                 "Đà Nẵng",
                 "Hải Phòng",
                 "Hà Nội",
                 "Hồ Chí Minh"}

    def parse_single_address(self, string):
        if string in self.provinces:
            return string

        for p in self.provinces:
            idx = string.find(p)
            if idx == -1:
                continue
            else:
                return p
        return string

    def parse_address(self, address):
        if type(address) is str:
            return self.parse_single_address(address)
        elif type(address) is list:
            addr = address[0]
            return self.parse_single_address(addr)

    def process_item(self, item, spider):
        item['address'] = self.parse_address(item['address'])
        return item


class NormalizeSalaryPipeline(object):

    @staticmethod
    def invert_format(string):
        result = None
        idx1_f = string.find(',')
        idx1_r = string.rfind(',')

        idx2_f = string.find('.')
        idx2_r = string.rfind('.')

        if idx1_f < 0 and idx2_f < 0:  # only number
            return float(string)

        elif idx2_f < 0:  # only contain ,
            last_number = len(string[idx1_r + 1:])
            if last_number < 3:
                return float(string[:idx1_r].replace(',', ''))
            else:
                return float(string.replace(',', ''))
        elif idx1_f < 0:  # only contain .
            last_number = len(string[idx2_r + 1:])
            if last_number < 3:
                return float(string[:idx2_r].replace('.', ''))
            else:
                return float(string.replace('.', ''))
        else:
            if idx1_r < idx2_r:  # . is phan thap phan
                return float(string.replace(',', ''))
            else:  # , is phan thap phan
                return float(string.replace('.', '').replace(',', '.'))

    @staticmethod
    def parse_salary(salary):
        if type(salary) is list:
            if len(salary) == 0:
                pass
            elif len(salary) == 1:
                return {
                    "min": -1,
                    "max": -1,
                    "unit": salary[0]
                }
            elif len(salary) == 2:
                if salary[-1] == 'USD':
                    return {
                        "min": NormalizeSalaryPipeline.invert_format(salary[0]) * 23360,
                        "max": 0,
                        "unit": "VNĐ"
                    }
                else:
                    return {
                        "min": NormalizeSalaryPipeline.invert_format(salary[0]),
                        "max": 0,
                        "unit": "VNĐ"
                    }
            elif len(salary) == 3:
                return {
                    "min": NormalizeSalaryPipeline.invert_format(salary[0]),
                    "max": NormalizeSalaryPipeline.invert_format(salary[1]),
                    "unit": "VNĐ"
                }
            elif len(salary) == 4:
                return {
                    "min": NormalizeSalaryPipeline.invert_format(salary[0]),
                    "max": NormalizeSalaryPipeline.invert_format(salary[2]),
                    "unit": "VNĐ"
                }
        elif type(salary) is str:
            s = salary.split(' ')
            if s[0] == 'Trên':
                s[0] = "{}-0".format(s[1])
            elif s[0] == 'Dưới':
                s[0] = "0-{}".format(s[1])
            t = s[0].split('-')
            if s[1] == 'triệu':
                return {
                    "min": NormalizeSalaryPipeline.invert_format(t[0] + '000000'),
                    "max": NormalizeSalaryPipeline.invert_format(t[1] + '000000'),
                    "unit": "VNĐ"
                }

    def process_item(self, item, spider):
        item['salary'] = self.parse_salary(item['salary'])
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.urls = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls.add(item['url'])
            return item


class DuplicatesFilterPipeline(object):
    def __init__(self):
        self.main_source = 'careerbuilder'
        self.filted = list()
        self.jaro_winkler = JaroWinkler()

    def find_candidates(self, job_title):
        result_size_filted = self.size_filter(self.filted, job_title)
        result_prefix_filted = self.prefix_filter(result_size_filted, job_title, k=3)
        return result_prefix_filted

    @staticmethod
    def size_filter(data, job_title):
        t = 0.8
        lb = len(job_title) * t
        ub = len(job_title) / t
        results = []
        for job in data:
            len_y = len(job['job_title'])
            if lb <= len_y <= ub:
                results.append(job)
        return results

    @staticmethod
    def prefix_filter(data, job_title, k=None):
        job_title_words = job_title.split(' ')
        if k is None:
            k = int(len(job_title_words) / 2)
        n_overlap = 0
        results = []
        for y in data:
            for w in job_title_words:
                if w in y['job_title']:
                    n_overlap += 1
                    if n_overlap > k:
                        results.append(y)
                        break
        return results

    def process_item(self, item, spider):
        if item['source'] == self.main_source:
            self.filted.append(item)
            return item
        else:
            job_title_1 = item['job_title']
            address_1 = item['company_address']
            company_name_1 = item['company_name']

            candidates = self.find_candidates(job_title_1)
            sim = False
            sim_score = 0
            for i in candidates:
                job_title_2 = i['job_title']
                address_2 = i['company_address']
                company_name_2 = i['company_name']

                sim_score = 0.6 * self.jaro_winkler.similarity(job_title_1, job_title_2)
                sim_score += 0.2 * self.jaro_winkler.similarity(address_1, address_2)
                sim_score += 0.2 * self.jaro_winkler.similarity(company_name_1, company_name_2)

                if sim_score >= 0.9:
                    print(sim_score)
                    print(job_title_1 + '|||' + str(address_1) + '|||' + company_name_1 + '|||' + item['source'])
                    print(job_title_2 + '|||' + str(address_2) + '|||' + company_name_2 + '|||' + i['source'])
                    print("=========================================================")
                    sim = True
                    raise DropItem("Duplicate item found with sim score {}: {}".format(sim_score, item))
            if len(candidates) == 0:
                self.filted.append(item)
                return item

            if not sim:
                self.filted.append(item)
                return item



class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('raw_data/items3.jl', 'w', encoding='utf8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item




class MongoPipeline(object):

    collection_name = 'job_integration'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item