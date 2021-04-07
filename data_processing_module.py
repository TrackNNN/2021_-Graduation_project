import sys

import IO_processing_module as data_IO

attribute = ['rsp']
IntMin, IntMax = -sys.maxsize - 1, sys.maxsize


class DisplayDataBlock:
    def __init__(self):
        self.rsp = 0


def print_csv_data():
    data = data_IO.read_form_csv()
    print(data['rsp'][:2])


def get_display_data_block_slice():
    data = data_IO.read_form_csv()
    row_nums = data.shape[0]
    display_data_assemble_slice = []
    for index in range(row_nums):
        block = DisplayDataBlock()
        for attr in attribute:
            setattr(block, attr, data.get(attr)[index])
        display_data_assemble_slice.append(block)
    return display_data_assemble_slice


def get_attr_min_max_value(data_block_slice, attr_name):
    min_value = IntMax
    max_value = IntMin
    for data_block in data_block_slice:
        value = getattr(data_block, attr_name)
        min_value = min(min_value, value)
        max_value = max(max_value, value)
    return min_value, max_value


def print_attr(data_block_slice, attr_name):
    for data_block in data_block_slice:
        print(getattr(data_block, attr_name))
