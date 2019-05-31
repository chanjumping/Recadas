#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from Util.Log import logger
from ServerModel.TCPRequestHandler import TCPRequestHandler, TCPRequestHandlerForFile, ThreadedTCPServer
import threading
from Util.Gui import loop
from Util.ReadConfig import conf
from SaveModel.SaveMediaThread import SaveMediaThread
from ParseModel.Consumer import ParseComm, Consumer
from ParseModel.ParseGetMediaThread import GetMediaThread
from Util.GlobalVar import query_msg_queue
from ServerModel.WebServer import run_http_server


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
    logger.debug('【 Data Server 】 Server starting, waiting for connection ...')
    if conf.get_protocol_type() == 5:
        FILE_HOST = '192.168.100.100'
        FILE_PORT = 8080
        file_server = ThreadedTCPServer((FILE_HOST, FILE_PORT), TCPRequestHandlerForFile)
        file_server_thread = threading.Thread(target=file_server.serve_forever)
        file_server_thread.daemon = True
        file_server_thread.start()
        logger.debug('【 File Server 】 Server starting, waiting for connection ...')
    if conf.get_protocol_type() == 1:
        while not query_msg_queue.empty():
            query_msg_queue.get(block=False)
        from SaveModel.SaveLogThread import SaveLogThread
        save_log_thread = SaveLogThread('SaveLog Thread Start ...')
        save_log_thread.setDaemon(True)
        save_log_thread.start()
    elif conf.get_protocol_type() == 4:
        run_http_server_thread = threading.Thread(target=run_http_server, name='run_http_server', args=())
        run_http_server_thread.setDaemon(True)
        run_http_server_thread.start()
    consume_thread = Consumer('【 Data Server 】 Consumer Thread Start ...')
    consume_thread.setDaemon(True)
    consume_thread.start()
    save_thread = SaveMediaThread('【 Data Server 】 SaveMedia Thread Start ...')
    save_thread.setDaemon(True)
    save_thread.start()
    parse_thread = ParseComm('【 Data Server 】 Parse Thread Start ...')
    parse_thread.setDaemon(True)
    parse_thread.start()
    get_media_thread = GetMediaThread('【 Data Server 】 GetMedia Thread Start ...')
    get_media_thread.setDaemon(True)
    get_media_thread.start()

    loop()

    try:
        while True:
            wake_event.wait()
            break
    except KeyboardInterrupt:
        logger.debug('捕捉到CTRL+C中断信号。')


if __name__ == '__main__':
    main()
