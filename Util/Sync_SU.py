#!/usr/bin/env python
# -*- coding: utf-8 -*

import threading
from Util.Log import logger
from Util.ReadConfig import conf
from Util.GetTestData import GetTestData
from Util.GlobalVar import send_queue
import time
import os

lock = threading.Lock()


class SyncThread(threading.Thread):
    def __init__(self, name, rec_obj):
        threading.Thread.__init__(self)
        self.name = name
        self.rec_obj = rec_obj
        self.setName(self.name)

    def run(self):
        if conf.get_protocol_type() == 1:
            logger.debug(threading.current_thread().getName())
            conf_path = os.path.join('TestData', '苏标外设实时同步数据.xls')
            while self.rec_obj.isAlive:
                table = GetTestData(conf_path)
                table.open()
                test_point, data = table.get_excel_data()
                if ' ' in data:
                    data = ''.join(data.split())
                lock.acquire()
                send_queue.put(data)
                lock.release()
                time.sleep(0.5)
