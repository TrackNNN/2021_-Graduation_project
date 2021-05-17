import sys
import threading
import time
import IO_processing_module as data_IO
import model

GdbPattern = "gdb"
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
        now_esp = task_data.get('esp')
        now_ebp = task_data.get('ebp')
        now_task_ebp = task_data.get('task_ebp')
        now_task_esp = task_data.get('task_esp')

        # 获取对应的taskObj
        task_obj = LoadTaskDict.get(task_id)
        if not task_obj:
            task_obj = model.Task(
                task_id=task_id,
            )
        last_stack_info = None
        if task_obj.stack_infos:
            last_stack_info = task_obj.stack_infos[-1]

        stack_info = model.StackInfo()
        method_names = task_data.get('method_names')
        if last_stack_info:
            stack_info.add_method_infos(last_stack_info.method_infos)
            if len(last_stack_info.method_infos) > len(method_names):
                stack_info.method_infos = stack_info.method_infos[:-1]
            elif len(last_stack_info.method_infos) < len(method_names):
                stack_info.add_method_info(now_task_esp, now_task_ebp, now_esp, now_ebp, method_names[-1])
        else:
            # 目前了为了解决中断出现的情况
            if len(method_names) > 1:
                stack_info.add_method_info(now_task_esp, now_task_ebp, str(hex(int(now_ebp, 16) - 8)), "0x0",
                                           method_names[0])
            stack_info.add_method_info(now_task_esp, now_task_ebp, now_esp, now_ebp, method_names[-1])

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


# 获取要展示的数据
def get_task_info():
    show_info = ShowData[ShowDataIndex]
    task_obj = TaskDict.get(show_info.task_id)

    stack_info = task_obj.stack_infos[show_info.stack_idx]
    return build_show_info_resp(task_obj, stack_info)


def build_show_info_resp(task, stack_info):
    return {
        "task_id": task.task_id,
        "method_infos": [
            {
                "task_ebp": method_info.task_ebp,
                "task_esp": method_info.task_esp,
                'ebp': method_info.ebp,
                'esp': method_info.esp,
                'method': method_info.method,
            }
            for method_info in stack_info.method_infos
        ]
    }
