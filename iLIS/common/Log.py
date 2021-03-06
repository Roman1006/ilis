# -*- coding: utf-8 -*-
# @Time : 2020-07-17 17:19
# @Author : Roman
# @FileName : Log.py
# @Email : 13883575239@163.com
# @Software: PyCharm
import logging
import threading
import os
from datetime import datetime
import codecs
# os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
proDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
# print(proDir)
class Log:
    def __init__(self):
        # 纯log日志目录
        logspath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
        # 定义log文件名称，以格式化时间命名
        logPath = os.path.join(logspath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        # 判断logPath目录是否存在，如果不存在则创建
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # 判断testlogpath文件是否存在，不存在则创建
        log_name = os.path.join(logPath, str(datetime.now().strftime("%Y%m%d%H%M%S")) + "__test_log.txt")
        if not os.path.exists(log_name):
            open(log_name, 'w')
        log_sent = os.path.join(logspath,str(datetime.now().strftime("%Y%m%d%H%M%S")) + "__test_log.txt")
        if not os.path.exists(log_sent):
            open(log_sent, 'w')
        # 生成self.logger对象
        self.logger = logging.getLogger()
        # 设定logger等级
        self.logger.setLevel(logging.INFO)
        # 定义handler 写入文件
        # handler = logging.FileHandler(os.path.join(logPath, log_name))
        loghandler = logging.FileHandler(log_sent)
        # 定义formatter 显示在控制台
        chandler = logging.StreamHandler()
        chandler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        chandler.setFormatter(formatter)
        loghandler.setFormatter(formatter)



        # self.logger.addHandler(handler)
        self.logger.addHandler(chandler)
        self.logger.addHandler(loghandler)



    def get_logger(self):
        return self.logger
class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")
    # file = codecs.open("create_log.log", 'r', 'utf-8')
