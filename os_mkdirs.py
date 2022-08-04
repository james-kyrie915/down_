# -*- coding:utf-8 -*-
import os
# remote_dir = "/home/download/"
# remote_dir = remote_dir[0:-1]
# print(remote_dir)
# local_filepath = r"E:\Pycharm_file\Data_collection\para\auto_makedir"
# if not os.path.exists(local_filepath):
#     os.makedirs(r"E:\Pycharm_file\Data_collection\para\auto_makedir")
# print(os.path.abspath(local_filepath))
# print("abcdefa".replace('a', 'z'))
# file = "/home/download_file/micro_class5.mp4"
# remote_dir = "/home/download_file"
# local_dir = r"E:\Pycharm_file\Data_collection\para\auto_makedir"
#
# print("os.path.dirname(remote_dir) = " + os.path.dirname(remote_dir))
# # print(local_dir.split('\\')[-1])
# local_filename = file.replace(remote_dir, local_dir).replace('/', '\\')
# print("local_filename = " + local_filename)
# local_filepath = os.path.dirname(local_filename)
# print("local_filepath = " + local_filepath)
# print("window.open('" + "" + "')")
# selenium启动浏览器多个窗口
import time

from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# def func1():
#     print("----------------")


# # @logger.catch()
# def func():
#     func1()
#     print(time.ctime())

#
# if __name__ == '__main__':
#     sched = BlockingScheduler()
#     # sched = BackgroundScheduler()
#
#     cronTrigger = CronTrigger(hour=0, minute=7, second=40, timezone='Asia/Shanghai')
#     # cronTrigger = CronTrigger(second=3, timezone='Asia/Shanghai')
#     sched.add_job(func, cronTrigger, id='my_job')
#
#     # intervalTrigger = IntervalTrigger(seconds=3, timezone='Asia/Shanghai')
#     # sched.add_job(func, intervalTrigger, id='my_job')
#     sched.start()
import sys
import os
cur_path = os.path.abspath('.')
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
print(cur_path)
print(root_path)
print(os.path.dirname(cur_path))
