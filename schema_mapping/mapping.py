import json


def read_mapping(file):
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

    return mappings


def read_data(file):
    results = []
    with open(file, 'r') as f:
        while True:
            row = f.readline()
            if row == '':
                break
            row = row[:-1]
            results.append(json.loads(row))
    return results


def add_fields(row, fields):
    results = ""
    for field in fields:
        results += str(row[field]) + ', '

    return results


def mapping_data(mapping, data):
    target = []
    for row in data:
        t = {}
        for m in mapping:
            if m[0] == 'source':
                t[m[0]] = m[1]
                continue

            if type(m[1]) is list:
                t[m[0]] = add_fields(row, m[1])
            elif m[1] == '':
                t[m[0]] = ''
            else:
                t[m[0]] = row[m[1]]
        # print(t)
        target.append(t)

    return target


def mapping_and_save(mapping, data, file_name):
    mapped = mapping_data(mapping, data)
    with open(file_name, 'a', encoding='utf8') as f:
        for row in mapped:
            f.write(json.dumps(row) + '\n')


sources = ['careerbuilder', 'careerlink', 'timviecnhanh']
for source in sources:
    mapping = read_mapping('schema_mapping')

    raw_data = read_data('../raw_data/' + source + '.jl')
    # for i in raw_data:
    #     print(i['address'])

    # target = mapping_data(mapping[source], raw_data)
    # print(len(target))
    mapping_and_save(mapping[source], raw_data, '../raw_data/mapped_test.jl')
