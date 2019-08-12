#! /usr/bin/env python
# coding=utf-8


# import logging
import logging.handlers
import os

logger = logging.getLogger('my_logger')
log_event = logging.getLogger('log_event')

if not os.path.exists('Logs'):
    os.makedirs('Logs')

logger.setLevel(logging.DEBUG)
log_event.setLevel(logging.DEBUG)

if os.listdir('Logs'):
    m = max([int(x.split('.')[0][3:]) for x in os.listdir('Logs') if 'file' not in x])
else:
    m = 0

# 创建一个handler，用于写入日志文件
fh = logging.handlers.RotatingFileHandler(r'Logs/log{}.log'.format(m + 1), maxBytes=104857600, backupCount=50)
fh.setLevel(logging.DEBUG)
fh_ev = logging.handlers.RotatingFileHandler(r'Logs/log_file{}.log'.format(m + 1), maxBytes=104857600, backupCount=50)
fh_ev.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch_ev = logging.StreamHandler()
ch_ev.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
fh_ev.setFormatter(formatter)
ch_ev.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# log_event.addHandler(fh)
log_event.addHandler(ch)
log_event.addHandler(fh_ev)
log_event.addHandler(ch_ev)








# FOREGROUND_WHITE = 0x0007
# FOREGROUND_BLUE = 0x01 # text color contains blue.
# FOREGROUND_GREEN = 0x02 # text color contains green.
# FOREGROUND_RED = 0x04 # text color contains red.
# FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
#
# STD_OUTPUT_HANDLE = -11
# std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
#
#
# def set_color(color, handle=std_out_handle):
#     b = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
#     return b
#
#
# class Logger:
#     def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
#         self.logger = logging.getLogger(path)
#         self.logger.setLevel(logging.DEBUG)
#         fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
#         # 设置CMD日志
#         sh = logging.StreamHandler()
#         sh.setFormatter(fmt)
#         sh.setLevel(clevel)
#         # 设置文件日志
#         fh = logging.FileHandler(path)
#         fh.setFormatter(fmt)
#         fh.setLevel(Flevel)
#         self.logger.addHandler(sh)
#         self.logger.addHandler(fh)
#
#     def debug(self, message):
#         self.logger.debug(message)
#
#     def info(self, message):
#         self.logger.info(message)
#
#     def war(self, message, color=FOREGROUND_YELLOW):
#         set_color(color)
#         self.logger.warning(message)
#         set_color(FOREGROUND_WHITE)
#
#     def error(self, message, color=FOREGROUND_RED):
#         set_color(color)
#         self.logger.error(message)
#         set_color(FOREGROUND_WHITE)
#
#     def cri(self, message):
#         self.logger.critical(message)
#
#
# if __name__ == '__main__':
#     logyyx = Logger('yyx.log',logging.WARNING, logging.DEBUG)
#     logyyx.debug('一个debug信息')
#     logyyx.info('一个info信息')
#     logyyx.war('一个warning信息')
#     logyyx.error('一个error信息')
#     logyyx.cri('一个致命critical信息')