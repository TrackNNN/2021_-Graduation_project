import csv

import pandas as pd

RegSeparator = "--------------------------------------------------------------------------[regs]"
csv_file_path = "data.csv"
gdb_file_path = "30days-stack_alloc.txt"
attr_list = ['EBP', 'ESP']


def read_from_csv():
    csv_data = pd.read_csv(csv_file_path, low_memory=False)
    csv_df = pd.DataFrame(csv_data)
    return csv_df


def write_to_csv(data):
    f = open('data.csv', 'w')
    csv_writer = csv.writer(f)
    # 写入头部和数据体
    csv_writer.writerow(attr_list)
    csv_writer.writerow(data)
    f.close()


def read_from_txt():
    f = open(gdb_file_path, "r")  # 打开
    line = f.readline()
    data = dict()
    while line:  # 直到读取完文件
        line = f.readline()  # 读取一行文件，包括换行符
        str_line = delete_line_wrap(str(line))
        if str_line == RegSeparator:
            lines_count = 3
            all_info = ""
            while lines_count:
                reg_line = str(f.readline())
                all_info += delete_line_wrap(reg_line)
                lines_count = lines_count - 1
            data = process_all_info(data, all_info)
    # print_dict(data)
    f.close()
    return data


def process_all_info(data, all_info):
    all_info += " "
    begin, end = 0, len(all_info)
    for idx in range(len(all_info)):
        character = all_info[idx]
        if character == ":":
            attr, attr_data = "", ""
            attr_idx, attr_data_idx = idx - 1, idx + 2
            add_char = True
            while add_char:
                add_char = False
                if check_char(all_info[attr_idx], attr_idx, begin, end):
                    attr = all_info[attr_idx] + attr
                    attr_idx = attr_idx - 1
                    add_char = True
                if check_char(all_info[attr_data_idx], attr_data_idx, begin, end):
                    attr_data = attr_data + all_info[attr_data_idx]
                    attr_data_idx = attr_data_idx + 1
                    add_char = True
            if attr in attr_list:
                attr_data_list = data.get(attr)
                if attr_data_list is None:
                    attr_data_list = []
                attr_data_list.append(attr_data)
                data.update({attr: attr_data_list})
    return data


def check_char(character, idx, begin, end):
    return end > idx >= begin and character != ' ' and character != '\n'


def delete_line_wrap(line):
    if line and line[-1] == '\n':
        line = line[:-1]
    return line


def print_dict(data):
    for attr, attr_data_list in data.items():
        print(attr, ":")
        for attr_data in attr_data_list:
            print(attr_data)
