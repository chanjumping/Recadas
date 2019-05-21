#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from Util.Log import logger
from ServerModel.TCPRequestHandler import TCPRequestHandler, ThreadedTCPServer
import threading
from Util.Gui import loop
from Util.ReadConfig import conf
from SaveModel.SaveMediaThread import SaveMediaThread

path = os.path.realpath(__file__)
sep = os.sep
wake_event = threading.Event()


def main():
    HOST = conf.get_address()
    PORT = conf.get_port()

    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.debug('Server starting, waiting for connection ...')
    save_thread = SaveMediaThread('SaveMedia Thread Start ...')
    save_thread.setDaemon(True)
    save_thread.start()

    loop()

    try:
        while True:
            wake_event.wait()
            break
    except KeyboardInterrupt:
        logger.debug('捕捉到CTRL+C中断信号。')


if __name__ == '__main__':
    main()
