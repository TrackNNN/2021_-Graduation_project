import sys
import threading
import time
import IO_processing_module as data_IO
import model

GdbPattern = "gdb"
IntMin, IntMax = -sys.maxsize - 1, sys.maxsize
ReservePercent = 0.15
HexBase, DecBase = 16, 10
ShowData = []
ShowDataIndex = 0
TaskDict = {}


class MyThread(threading.Thread):
    def __init__(self, pattern, parse_interval):
        threading.Thread.__init__(self)
        self.parse_interval = parse_interval
        self.pattern = pattern

    def run(self):
        print("开始定时解析日志:path %s", data_IO.gdb_log_path)
        parse_log_task(self.pattern, self.parse_interval)
        print("退出线程")


# 定时解析日志更新对应的数组
def parse_log_task(pattern, parse_time):
    global ShowData
    global TaskDict
    while True:
        ShowData, TaskDict = set_file_data(pattern)
        time.sleep(parse_time)


def set_file_data(parse_pattern):
    record_nums = 0
    file_data = {}
    if parse_pattern == GdbPattern:
        file_data = data_IO.read_from_txt()
        attr = data_IO.Log2ClassAttrMap.get(data_IO.LogAttrList[0])
        record_nums = len(file_data[attr])

    # 更新task_dict
    LoadingData = []
    LoadTaskDict = {}
    for idx in range(record_nums):
        task_data = get_attr_dict(file_data, idx)

        task_id = task_data.get('task_id')
        now_esp, now_ebp = task_data.get('esp'), task_data.get('ebp')
        stack_info = model.StackInfo()
        for method_name in task_data.get('method_names'):
            stack_info.add_method_info(method=method_name, esp=now_esp, ebp=now_ebp)  # todo

        # 获取对应的taskObj
        task_obj = LoadTaskDict.get(task_id)
        if not task_obj:
            task_obj = model.Task(
                task_id=task_id,
                task_ebp=task_data.get('task_ebp'),
                task_esp=task_data.get('task_esp'),
            )
        # 添加当前栈的信息
        task_obj.add_stack_info(stack_info)

        # 加入新加的数据
        LoadingData.append(model.ShowInfo(
            task_id=task_obj.task_id,
            stack_idx=task_obj.info_len - 1,
        ))
        LoadTaskDict[task_id] = task_obj

    return LoadingData, LoadTaskDict


def get_attr_dict(data_dict, idx):
    """
    :param data_dict:
    :param idx:
    :return: {
        task_id: id1,
        task_ebp: task_ebp1,
        task_esp: task_esp1,
        esp: esp1,
        ebp: ebp1,
        method_names: [method1,method2,...]
    }
    """
    result = {
        "task_id": data_dict.get('task_id')[idx],
        "task_ebp": data_dict.get('task_ebp')[idx],
        "task_esp": data_dict.get('task_esp')[idx],
        "esp": data_dict.get('esp')[idx],
        "ebp": data_dict.get('ebp')[idx],
        "method_names": data_dict.get('method_names_list')[idx],
    }

    return result


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


def Str_Hex_To_Dec_Num(Hex_Str):
    if Hex_Str[:2] == "0X":
        Hex_Str = Hex_Str[2:]
    return int(Hex_Str, HexBase)


# 获取要展示的数据
def get_task_info():
    show_info = ShowData[ShowDataIndex]
    task_obj = TaskDict.get(show_info.task_id)

    stack_info = task_obj.stack_infos[show_info.stack_idx]
    return build_show_info_resp(task_obj, stack_info)


def build_show_info_resp(task, stack_info):
    return {
        "task_id": task.task_id,
        "task_ebp": task.task_ebp,
        "task_esp": task.task_esp,
        "method_infos": [
            {
                'ebp': method_info.ebp,
                'esp': method_info.esp,
                'method': method_info.method,
            }
            for method_info in stack_info.method_infos[::-1]
        ]
    }
