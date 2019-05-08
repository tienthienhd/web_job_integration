import json


def read_file(file):
    salary = []
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            job = json.loads(line)
            salary.append(job['salary'])

    return salary


def invert_format(string):
    result = None
    idx1_f = string.find(',')
    idx1_r = string.rfind(',')

    idx2_f = string.find('.')
    idx2_r = string.rfind('.')

    if idx1_f < 0 and idx2_f < 0: # only number
        return float(string)

    elif idx2_f < 0: # only contain ,
        last_number = len(string[idx1_r+1:])
        if last_number < 3:
            return float(string[:idx1_r].replace(',', ''))
        else:
            return float(string.replace(',', ''))
    elif idx1_f < 0: # only contain .
        last_number = len(string[idx2_r + 1:])
        if last_number < 3:
            return float(string[:idx2_r].replace('.', ''))
        else:
            return float(string.replace('.', ''))
    else:
        if idx1_r < idx2_r: # . is phan thap phan
            return float(string.replace(',', ''))
        else: # , is phan thap phan
            return float(string.replace('.', '').replace(',', '.'))


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
                    "min": invert_format(salary[0]) * 23220,
                    "max": 0,
                    "unit": "VNĐ"
                }
            else:
                return {
                    "min": invert_format(salary[0]),
                    "max": 0,
                    "unit": "VNĐ"
                }
        elif len(salary) == 3:
            return {
                "min": invert_format(salary[0]),
                "max": invert_format(salary[1]),
                "unit": "VNĐ"
            }
        elif len(salary) == 4:
            return {
                "min": invert_format(salary[0]),
                "max": invert_format(salary[2]),
                "unit": "VNĐ"
            }
    elif type(salary) is str:
        s = salary.split(' ')
        if s[0] == 'Trên':
            s[0] = "{}-0".format(s[1])
        elif s[0] == 'Dưới':
            s[0] = "0-{}".format(s[1])
        t = s[0].split('-')


        if s[-1] == 'triệu':
            return {
                "min": invert_format(t[0]+'000000'),
                "max": invert_format(t[1]+'000000'),
                "unit": "VNĐ"
            }



a = read_file('../raw_data/mapped_test.jl')


for i in a:
    print(parse_salary(i))