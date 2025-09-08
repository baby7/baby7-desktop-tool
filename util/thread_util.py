# 关闭单个线程
def close_one_thread(thread):
    if thread is not None:
        thread.active = False
        thread.terminate()
        thread.quit()
        thread.wait()
    while True:
        if thread is None or thread.isFinished() is True:
            break
        thread.active = False
        thread.terminate()
        thread.quit()
        thread.wait()
