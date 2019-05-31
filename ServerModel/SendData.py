#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.Log import logger
import threading
import time
from ParseModel import ParseData


class SendData(threading.Thread):
    def __init__(self, name, rec_obj):
        threading.Thread.__init__(self)
        self.name = name
        self.rec_obj = rec_obj
        self.setName(self.name)

    def run(self):
        logger.debug(threading.current_thread().getName())
        while self.rec_obj.isAlive:
            text = ParseData.send_queue_data()
            if text:
                try:
                    self.rec_obj.request.sendall(text)
                except TimeoutError:
                    logger.debug('Receiving ack timeout，connection is interrupted.')
                except ConnectionResetError:
                    logger.debug('ConnectionResetError，connection is interrupted.')
                except ConnectionAbortedError:
                    logger.debug('ConnectionAbortedError，connection is interrupted.')
                except OSError:
                    logger.debug('SEND DATA THREAD {}'.format(self.rec_obj.request))
            time.sleep(0.001)
