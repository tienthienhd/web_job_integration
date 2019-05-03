import json

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

def read_file(file):
    categories = []
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            job = json.loads(line)
            categories.append(job['address'])
            # if len(job['company_address']) < 2:
            #     print(job['source'])
            # print(str(job['address']) + "||||" + str(job['company_address']))
    return categories


def parse_single_address(string):
    if string in provinces:
        return string

    for p in provinces:
        idx = string.find(p)
        if idx == -1:
            continue
        else:
            return p
    return string


def parse_address(address):
    if type(address) is str:
        return parse_single_address(address)
    elif type(address) is list:
        addr = address[0]
        return parse_single_address(addr)


# a = parse_address(['viec lam tai hà nội '])
# print(a)

# a = read_file('../raw_data/mapped_test.jl')
# for j in a:
#     print(j)
#     addr = parse_address(j)
#     # if addr is None:
#     #     print(j)
#     print(addr)
# b = combine(a)
# b = sorted(b)
# for i in b:
#     print(i)

