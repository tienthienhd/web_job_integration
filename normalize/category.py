import json


def read_file(file):
    salary = []
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            job = json.loads(line)
            salary.append(job['categories'])

    return salary


a = read_file('../raw_data/mapped_test.jl')

categories = []
for i in a:
    for j in i:
        j = j.lower()
        if j not in categories:
            categories.append(j)

for i in categories:
    print(i.capitalize())