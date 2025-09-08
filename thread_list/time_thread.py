# -- coding: utf-8 --
import time
import datetime
import traceback
from PySide2.QtCore import QThread, Signal


# 定时线程(一分钟提醒一次)
class TimeThread(QThread):
    active = True
    # 触发器
    zero_trigger = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def stop(self):
        self.terminate()

    def run(self):
        while self.active:
            try:
                time.sleep(0.5)
                datetime_now = datetime.datetime.now()
                second = datetime_now.second
                if int(second) == 0:
                    self.zero_trigger.emit(str(datetime_now.strftime("%Y-%m-%d %H:%M:%S")))
                    time.sleep(2)
            except Exception:
                traceback.print_exc()
