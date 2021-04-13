# import sys
#
# from PyQt5.QtWidgets import QApplication
# from View_module import MainForm
#
#
# def __main__():
#     app = QApplication(sys.argv)
#     form = MainForm()
#     form.resize(1200, 800)
#     form.show()
#     app.exec_()

# from PySide2.QtWidgets import QApplication
# from PySide2.QtUiTools import QUiLoader
#
#
# class StackGraph:
#     def __init__(self):
#         self.ui = QUiLoader().load('stack.ui')
#         # 1 获取数据展示到UI上
#         # 2 实现点击功能来进行图形的重新展示
#         # 3 对于空白单位的填写
#         # 4 中期检查报告编写
#         # 5 PPT编写
#
# app = QApplication([])
# stats = StackGraph()
# stats.ui.show()
# app.exec_()

import data_processing_module as IO_Module

IO_Module.get_data_block_slice("gdb")
