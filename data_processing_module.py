import sys

import IO_processing_module as data_IO

attr_list = ['ESP', 'EBP']
GdbPattern, CsvPattern = "gdb", "csv"
IntMin, IntMax = -sys.maxsize - 1, sys.maxsize
ReservePercent = 0.15


class DataBlock:
    def __init__(self):
        self.ESP = 0
        self.EBP = 0


def get_data_block_slice(Pattern):
    row_nums = 0
    if Pattern == GdbPattern:
        data = data_IO.read_from_txt()
        row_nums = len(data[attr_list[0]])
    elif Pattern == CsvPattern:
        data = data_IO.read_form_csv()
        row_nums = data.shape[0]
    data_block_slice = []
    for index in range(row_nums):
        block = DataBlock()
        for attr in attr_list:
            setattr(block, attr, data.get(attr)[index])
        data_block_slice.append(block)
    print_data_blocks(data_block_slice)
    return data_block_slice


def get_attr_min_max_value(data_block_slice, attr_name):
    min_value = IntMax
    max_value = IntMin
    for data_block in data_block_slice:
        value = getattr(data_block, attr_name)
        min_value = min(min_value, value)
        max_value = max(max_value, value)
    return min_value, max_value


def get_attr_interval(data_block_slice, attr_name):
    min_value, max_value = get_attr_min_max_value(data_block_slice, attr_name)
    reserve_value = int((max_value - min_value) * ReservePercent)
    return min_value - reserve_value, max_value + reserve_value


def print_attr(data_block_slice, attr_name):
    for data_block in data_block_slice:
        print(getattr(data_block, attr_name))


def print_data_blocks(data_block_slice):
    idx = 0
    for data_block in data_block_slice:
        for attr_name in attr_list:
            print(attr_name, ":", getattr(data_block, attr_name))
        print(idx)
        idx += 1
