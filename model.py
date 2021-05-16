class ShowInfo:
    def __init__(self,task_id,stack_idx):
        self.task_id = task_id
        self.stack_idx = stack_idx


class Task:
    def __init__(self, task_id, task_esp, task_ebp):
        self.task_id = task_id
        self.stack_infos = []
        self.info_len = 0
        self.task_esp = task_esp
        self.task_ebp = task_ebp

    def add_stack_info(self, stack_info):
        self.stack_infos.append(stack_info)
        self.info_len = len(self.stack_infos)


class StackInfo:
    def __init__(self):
        self.method_infos = []

    def add_method_info(self, method, esp, ebp):
        self.method_infos.append(MethodInfo(
            esp=esp,
            ebp=ebp,
            method=method,
        ))


class MethodInfo:
    def __init__(self, esp, ebp, method):
        self.esp = esp
        self.ebp = ebp
        self.method = method
