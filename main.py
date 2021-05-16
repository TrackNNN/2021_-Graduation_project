import data_processing_module as pcs
from PyQt5.QtWidgets import QApplication
import sys
from View_module import MyWindow
ParseFileMode = "gdb"
ParseFileTime = 10

def __main__():
    # 定时解析日志
    parse_log_thread = pcs.MyThread(ParseFileMode, ParseFileTime)
    parse_log_thread.start()

    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())


__main__()
