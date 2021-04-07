import sys

from PyQt5.QtWidgets import QApplication
from View_module import MainForm

app = QApplication(sys.argv)
form = MainForm()
form.resize(1200, 800)
form.show()
app.exec_()

# import data_processing_module  as data_module
#
# Slice = data_module.get_display_data_block_slice()
# data_module.print_attr(Slice, "rsp")
# print(data_module.get_attr_min_max_value(Slice, 'rsp'))
