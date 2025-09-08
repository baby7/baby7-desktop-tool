#! /usr/bin/env python
# coding=gbk
import logging


class Logger:
    def __init__(self, path, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        # 设置文件日志
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(file_level)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        print(message)
        self.logger.debug(message)

    def info(self, message):
        print(message)
        self.logger.info(message)

    def war(self, message):
        print(message)
        self.logger.warn(message)

    def error(self, message):
        print(message)
        self.logger.error(message)

    def cri(self, message):
        print(message)
        self.logger.critical(message)
