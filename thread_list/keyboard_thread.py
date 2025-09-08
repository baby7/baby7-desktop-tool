# -- coding: utf-8 --
from pynput import keyboard
from PySide2.QtCore import QThread, Signal


ALT = False
# Q = False
ONE = False


# 本文中只用到ALT和C其他的备用（在我的小工具包里ALT+Z是截屏、ALT+x是截屏文字识别）自行扩展
def listen(keyboard_trigger):  # 键盘监听函数
    # def on_press(key):
    #     global ALT, Q
    #     if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
    #         ALT = True
    #     if key == keyboard.KeyCode(char='q') or key == keyboard.KeyCode(char='Q'):
    #         Q = True
    #
    #     if ALT and Q:  # 检测到Alt和c同时按下时
    #         Q = False
    #         keyboard_trigger.emit("11")
    def on_press(key):
        global ALT, ONE
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            ALT = True
        if key == keyboard.KeyCode(char='1'):
            ONE = True

        if ALT and ONE:  # 检测到Alt和c同时按下时
            ONE = False
            keyboard_trigger.emit("11")

    # def on_release(key):
    #     global ALT, Q
    #     if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
    #         ALT = False
    #     if key == keyboard.KeyCode(char='q') or key == keyboard.KeyCode(char='Q'):
    #         Q = False

    def on_release(key):
        global ALT, ONE
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            ALT = False
        if key == keyboard.KeyCode(char='1'):
            ONE = False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 键盘监听线程
class KeyboardThread(QThread):
    active = True
    # 触发器
    keyboard_trigger = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def stop(self):
        self.terminate()

    def run(self):
        while self.active:
            listen(self.keyboard_trigger)
