#! /usr/bin/env python
# coding=utf-8

import socketserver
from Util.Log import logger
import time
import socket
from Util.ReadConfig import conf
from ParseModel import ParseData
from ServerModel.SendData import SendData


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        if conf.get_protocol_type() == 1:
            self.timeOut = None
        else:
            self.timeOut = 20
        self.remain = b''
        self.isAlive = True
        self.request.settimeout(self.timeOut)

    def handle(self):
        address, port = self.client_address
        logger.debug('【 Data Server 】 Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('【 Data Server 】 Producer Thread Start ...')
        send_thread = SendData('【 Data Server 】 Send Thread Start ...', self)
        send_thread.setDaemon(True)
        send_thread.start()

        if conf.get_protocol_type() == 1:
            if conf.get_sync_flag():
                from Util.Sync_SU import SyncThread
                sync_thread = SyncThread('Sync Thread Start ...', self)
                sync_thread.setDaemon(True)
                sync_thread.start()
            global fetch_media_flag
            fetch_media_flag = True

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce(buf, self.remain)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    logger.debug('【 Data Server 】 Receiving ack timeout，connection is interrupted.')
                except ConnectionResetError:
                    logger.debug('【 Data Server 】 ConnectionResetError，connection is interrupted.')
                except ConnectionAbortedError:
                    logger.debug('【 Data Server 】 ConnectionAbortedError，connection is interrupted.')
            except socket.timeout:
                break
            if not buf:
                self.isAlive = False
                time.sleep(0.1)
                logger.debug('【 Data Server 】 Receive empty data，connection is interrupted.')
                break
            self.remain = ParseData.produce(buf, self.remain)
            time.sleep(0.001)

    def finish(self):
        address, port = self.client_address
        logger.debug('【 Data Server 】 Connection {} {} is disconnected.'.format(address, port))
        logger.debug('='*100)
        logger.debug('='*100)
        logger.debug('='*100)


class TCPRequestHandlerForFile(socketserver.BaseRequestHandler):

    def setup(self):
        self.timeOut = 20
        self.remain = b''
        self.isAlive = True
        self.request.settimeout(self.timeOut)

    def handle(self):
        address, port = self.client_address
        logger.debug('【 File Server 】 Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('【 File Server 】 Producer Thread Start ...')
        send_thread = SendData('【 File Server 】 Send Thread Start ...', self)
        send_thread.setDaemon(True)
        send_thread.start()

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce(buf, self.remain)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    logger.debug('【 File Server 】 Receiving ack timeout，connection is interrupted.')
                except ConnectionResetError:
                    logger.debug('【 File Server 】 ConnectionResetError，connection is interrupted.')
                except ConnectionAbortedError:
                    logger.debug('【 File Server 】 ConnectionAbortedError，connection is interrupted.')
            except socket.timeout:
                break
            if not buf:
                self.isAlive = False
                time.sleep(0.1)
                logger.debug('【 File Server 】 Receive empty data，connection is interrupted.')
                break
            self.remain = ParseData.produce(buf, self.remain)
            time.sleep(0.001)

    def finish(self):
        address, port = self.client_address
        logger.debug('【 File Server 】 Connection {} {} is disconnected.'.format(address, port))
        logger.debug('-'*100)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
