# -- coding: utf-8 --
import time
import datetime
import traceback
from PySide2.QtCore import QThread, Signal
from get_info import get_schedule_info


# 定时更新倒计时
class ScheduleThread(QThread):
    active = True
    first = True
    # 触发器
    important_trigger = Signal(str)
    daily_trigger = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def stop(self):
        self.terminate()

    def run(self):
        while self.active:
            try:
                time.sleep(0.5)
                datetime_now = datetime.datetime.now()
                minute = datetime_now.minute
                if int(minute) % 5 == 0 or self.first:
                    self.first = False
                    # 重要的
                    important_schedule_list = get_schedule_info.get_important_schedule_list()
                    important_schedule_text = ""
                    for now_follow_date_index in range(len(important_schedule_list)):
                        if now_follow_date_index < 7:
                            important_schedule_text += "还有" + str(important_schedule_list[now_follow_date_index]['gap_day']) + "天 " \
                                                    + important_schedule_list[now_follow_date_index]['task'] + "\n"
                    if important_schedule_text.endswith("\n"):
                        important_schedule_text = important_schedule_text[:-1]
                        self.important_trigger.emit(str(important_schedule_text))
                    # 日程
                    daily_schedule_list = get_schedule_info.get_daily_schedule_list()
                    daily_schedule_text = ""
                    for now_follow_date_index in range(len(daily_schedule_list)):
                        daily_schedule_text += "☑" if daily_schedule_list[now_follow_date_index]['state'] else "☐"
                        daily_schedule_text += daily_schedule_list[now_follow_date_index]['task'] + "\n"
                    if daily_schedule_text.endswith("\n"):
                        daily_schedule_text = daily_schedule_text[:-1]
                    self.daily_trigger.emit(str(daily_schedule_text))
                    time.sleep(2)
            except Exception:
                traceback.print_exc()
