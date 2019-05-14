#! /usr/bin/env python
# coding=utf-8

import socketserver
from Util.Log import logger
from Util.GlobalVar import *
from ParseModel.Consumer import Consumer, ParseComm
import time
import socket
from SaveModel.SaveMediaThread import SaveMediaThread
from ParseModel.ParseGetMediaThread import GetMediaThread
from Util.ReadConfig import conf
from ParseModel import ParseData
from ServerModel.WebServer import run_http_server


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.timeOut = 30
        self.remain = b''
        self.isAlive = True
        if not conf.get_protocol_type() == 1:
            self.request.settimeout(self.timeOut)

    def handle(self):
        address, port = self.client_address
        logger.debug('Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('Producer Thread Start ...')
        send_thread = threading.Thread(target=self.send, name='Send Thread Start ...')
        send_thread.setDaemon(True)
        send_thread.start()
        consume_thread = Consumer('Consumer Thread Start ...', self)
        consume_thread.setDaemon(True)
        consume_thread.start()
        parse_thread = ParseComm('Parse Thread Start ...', self)
        parse_thread.setDaemon(True)
        parse_thread.start()
        save_thread = SaveMediaThread('SaveMedia Thread Start ...', self)
        save_thread.setDaemon(True)
        save_thread.start()
        get_media_thread = GetMediaThread('GetMedia Thread Start ...', self)
        get_media_thread.setDaemon(True)
        get_media_thread.start()
        if conf.get_protocol_type() == 1:
            from SaveModel.SaveLogThread import SaveLogThread
            save_log_thread = SaveLogThread('SaveLog Thread Start ...', self)
            save_log_thread.setDaemon(True)
            save_log_thread.start()

            while not query_msg_queue.empty():
                query_msg_queue.get(block=False)
            if conf.get_sync_flag():
                from Util.Sync_SU import SyncThread
                sync_thread = SyncThread('Sync Thread Start ...', self)
                sync_thread.setDaemon(True)
                sync_thread.start()
            global fetch_media_flag
            fetch_media_flag = True
        elif conf.get_protocol_type() == 4:
            run_http_server_thread = threading.Thread(target=run_http_server, name='run_http_server', args=())
            run_http_server_thread.setDaemon(True)
            run_http_server_thread.start()

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce(buf, self.remain)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    logger.debug('Receiving ack timeout，connection is interrupted.')
                except ConnectionResetError:
                    logger.debug('ConnectionResetError，connection is interrupted.')
                except ConnectionAbortedError:
                    logger.debug('ConnectionAbortedError，connection is interrupted.')
            except socket.timeout:
                break
            if not buf:
                logger.debug('Receive empty data，connection is interrupted.')
                break
            self.remain = ParseData.produce(buf, self.remain)
            time.sleep(0.001)

    def send(self):
        logger.debug(threading.current_thread().getName())
        while self.isAlive:
            text = ParseData.send_queue_data()
            if text:
                self.request.sendall(text)
            time.sleep(0.001)

    def finish(self):
        self.isAlive = False
        address, port = self.client_address
        logger.debug('Connection {} {} is disconnected.'.format(address, port))
        logger.debug('-'*100)
        logger.debug('-'*100)
        logger.debug('-'*100)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
