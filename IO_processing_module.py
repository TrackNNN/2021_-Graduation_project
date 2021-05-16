import csv
import pandas as pd

# todo 写到Constant

csv_file_path = "data.csv"
gdb_log_path = "C:/Users/98074/Desktop/debugInfo/30days-stack_alloc.txt"
RegSeparator = "--------------------------------------------------------------------------[regs]"
BtSeparator = "----------------back_trace---------------"
TssSeparator = "  tss = {"
FifoSeparator = "  fifo = {"

SeparatorSet = [RegSeparator, TssSeparator, FifoSeparator]
LogAttrList = ['EBP', 'ESP', 'task', 'esp', 'ebp']

Log2ClassAttrMap = {
    'EBP': 'ebp',
    'ESP': 'esp',
    'task': 'task_id',
    'esp': 'task_esp',
    'ebp': 'task_ebp'
}

TailChar = [',', ' ', '\n']
HeadChar = [' ']
SectionSymbol = 0
SectionSubLeft = 1
SectionAddRight = 2

symbolSectionDict = {
    RegSeparator: (':', 1, 2),
    TssSeparator: ('=', 2, 2),
    FifoSeparator: ('=', 2, 2),
}

catLineCountDict = {
    RegSeparator: 3,
    TssSeparator: 26,
    FifoSeparator: 7,
}


def read_from_csv():
    csv_data = pd.read_csv(csv_file_path, low_memory=False)
    csv_df = pd.DataFrame(csv_data)
    return csv_df


def read_from_txt():
    """
    :return:
    {
         'task_id': [1, 2, 3, 4],
         'task_esp': ["task_esp1", "task_esp2", "task_esp3", "task_esp4"],
         'task_ebp': ["task_ebp1", "task_ebp2", "task_ebp3", "task_ebp4"],
         'esp': ["esp1", "esp2", "esp3", "esp4"],
         'ebp': ["ebp1", "ebp2", "ebp3", "ebp4"],
         'method_names_list': [
             ["method1"],
             ["method1", "method2"],
             ["method1", "method2", "method3"],
             ["method1", "method2"],
         ]
     }
    """

    f = open(gdb_log_path, "r")  # 打开
    line = f.readline()
    data = dict()
    while line:  # 直到读取完文件
        line = f.readline()  # 读取一行文件，包括换行符
        str_line = delete_line_wrap(str(line))

        if str_line in SeparatorSet:
            Separator = str_line
            line_count = catLineCountDict.get(Separator)
            sectionInfo = symbolSectionDict.get(Separator)
            f, all_info = cat_info_str(f, line_count)
            data = process_all_info(data, all_info, sectionInfo[SectionSymbol], sectionInfo[SectionSubLeft],
                                    sectionInfo[SectionAddRight])
        elif str_line == BtSeparator:
            f, data = set_method_names(f, data)
    # print_dict(data)
    f.close()
    return data


def set_method_names(f, data):
    line = delete_line_wrap(str(f.readline()))
    method_names = []
    while line != BtSeparator:
        method_name = ""
        if line and line[0] == '#':
            left_idx, right_idx = 0, 0

            if line[1] == '0':
                left_idx = right_idx = 4
            elif line[18] != '?':
                left_idx = right_idx = 18

            # 当起点不为0的时候
            if right_idx:
                while line[right_idx] != ' ':
                    right_idx += 1
            method_name = line[left_idx:right_idx]

        # 将本次BT的函数进行添加
        if method_name:
            method_names.append(method_name)
        line = delete_line_wrap(str(f.readline()))

    # 将本次BT的内容写入数据
    method_names_list = data.get('method_names_list')
    if not method_names_list:
        method_names_list = []
    method_names_list.append(method_names)
    data['method_names_list'] = method_names_list
    return f, data


def cat_info_str(f, lines_count):
    all_info = ""
    while lines_count:
        line = str(f.readline())
        all_info += delete_line_head_tail(line)
        lines_count = lines_count - 1
    return f, all_info


# 删除回车
def delete_line_wrap(line):
    if line and line[-1] == '\n':
        line = line[:-1]
    return line


def delete_line_head_tail(line):
    tail_idx = len(line)
    head_idx = 0
    while tail_idx and line[tail_idx - 1] in TailChar:
        tail_idx -= 1
    while head_idx < tail_idx and line[head_idx] in HeadChar:
        head_idx += 1
    return " " + line[head_idx:tail_idx] + " "


def process_all_info(data, all_info, symbol, sub_idx, add_idx):
    all_info += " "
    begin, end = 0, len(all_info)
    # 删除掉
    for idx in range(len(all_info)):
        character = all_info[idx]

        if character == symbol:

            log_attr, attr_data = "", ""
            attr_idx, attr_data_idx = idx - sub_idx, idx + add_idx
            add_char = True

            while add_char:
                add_char = False

                if check_char(all_info[attr_idx], attr_idx, begin, end):
                    log_attr = all_info[attr_idx] + log_attr
                    attr_idx = attr_idx - 1
                    add_char = True

                if check_char(all_info[attr_data_idx], attr_data_idx, begin, end):
                    attr_data = attr_data + all_info[attr_data_idx]
                    attr_data_idx = attr_data_idx + 1
                    add_char = True

            if log_attr in LogAttrList:
                class_attr = Log2ClassAttrMap.get(log_attr)
                class_attr_data_list = data.get(class_attr)
                if class_attr_data_list is None:
                    class_attr_data_list = []
                class_attr_data_list.append(attr_data)
                # 更新数据
                data[class_attr] = class_attr_data_list
    return data


def check_char(character, idx, begin, end):
    return end > idx >= begin and character != ' ' and character != '\n'


def print_dict(data):
    for attr, attr_data_list in data.items():
        print(attr, ":")
        for attr_data in attr_data_list:
            print(attr_data)
