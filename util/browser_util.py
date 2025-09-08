import os


def open_url(url):
    os.popen('start ' + str(url))
