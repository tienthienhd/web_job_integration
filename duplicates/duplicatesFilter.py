import json
from similarity.normalized_levenshtein import NormalizedLevenshtein
from similarity.jarowinkler import JaroWinkler
from similarity.jaccard import Jaccard


normalized_levenshtein = NormalizedLevenshtein()
jaro_winkler = JaroWinkler()
jaccard = Jaccard(k=3)


def levenshtein_sim(s0, s1):
    return normalized_levenshtein.similarity(s0, s1)

def jaro_winkler_sim(s0, s1):
    return jaro_winkler.similarity(s0, s1)

def jaccard_sim(s0, s1):
    return jaccard.similarity(s0, s1)


def read_file(file):
    items = []
    with open(file, 'r', encoding='utf8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            try:
                job = json.loads(line)
            except json.decoder.JSONDecodeError:
                continue
            items.append(job)

    return items

# [job['job_title'], job['address'], job['company_name']]

main_source = 'careerbuilder'
filted = list()


inverted_index = {}
def gen_inverted_index(data):
    for job in data:
        job_title = job['job_title']
        job_title_words = job_title.split(' ')
        print(job_title_words)
        for w in job_title_words:
            if w not in inverted_index:
                inverted_index[w] = [job['idx']]
            else:
                if job['idx'] not in inverted_index[w]:
                    inverted_index[w].append(job['idx'])


def find_candidates(job_title):
    result_size_filted = size_filter(filted, job_title)
    result_prefix_filted = prefix_filter(result_size_filted, job_title, k=None)
    return result_prefix_filted


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


def duplicate_filter(item):
    if item['source'] == main_source:
        filted.append(item)
    else:
        job_title_1 = item['job_title']
        address_1 = item['company_address']
        company_name_1 = item['company_name']

        candidates = find_candidates(job_title_1)
        sim = False
        for i in candidates:
            job_title_2 = i['job_title']
            address_2 = i['company_address']
            company_name_2 = i['company_name']

            sim = 0.6 * jaro_winkler_sim(job_title_1, job_title_2)
            sim += 0.2 * jaro_winkler_sim(address_1, address_2)
            sim += 0.2 * jaro_winkler_sim(company_name_1, company_name_2)

            if sim >= 0.89:
                print(sim)
                print(job_title_1 + '|||' + str(address_1) + '|||' + company_name_1 + '|||' + item['source'])
                print(job_title_2 + '|||' + str(address_2) + '|||' + company_name_2 + '|||' + i['source'])
                print("=========================================================")
                sim = True
                break
        if not sim and len(candidates) == 0:
            filted.append(item)



a = read_file('../raw_data/mapped_test.jl')
# gen_inverted_index(a)
print(len(a))
for j in a:
    duplicate_filter(j)
#
print(len(a))
print(len(filted))