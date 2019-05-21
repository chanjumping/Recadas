#!/usr/bin/env python
# -*- coding: utf-8 -*

import configparser
import re
import os

path = os.path.realpath(__file__)
sep = os.sep
conf_path = os.path.join(os.getcwd(), 'conf.ini')


class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(conf_path, encoding='utf-8')

        self.sync_flag = True
        self.protocol_type = 1
        self.get_media_flag = True
        self.address = '192.168.100.100'
        self.port = 8888
        self.file_address = '103.46.128.43'
        self.file_port = 9090

    def get_config(self):
        content = open(conf_path, encoding='utf-8').read()
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)

        open('conf.ini', 'w', encoding='utf-8').write(content)
        config = configparser.ConfigParser()
        config.read('conf.ini', encoding='utf-8')
        self.set_protocol_type(config.getint('config', 'protocol_type'))
        self.set_sync_flag(config.getboolean('config', 'sync_data'))
        self.set_get_media_flag(config.getboolean('config', 'get_media'))
        self.set_address(config.get('config', 'address'))
        self.set_port(config.getint('config', 'port'))
        self.set_file_address(config.get('config', 'file_address'))
        self.set_file_port(config.getint('config', 'file_port'))

    def set_sync_flag(self, value):
        self.sync_flag = value

    def get_sync_flag(self):
        return self.sync_flag

    def set_protocol_type(self, value):
        self.protocol_type = value

    def get_protocol_type(self):
        return self.protocol_type

    def set_get_media_flag(self, value):
        self.get_media_flag = value

    def get_get_media_flag(self):
        return self.get_media_flag

    def set_address(self, value):
        self.address = value

    def get_address(self):
        return self.address

    def set_port(self, value):
        self.port = value

    def get_port(self):
        return self.port

    def set_file_address(self, value):
        self.file_address = value

    def get_file_address(self):
        return self.file_address

    def set_file_port(self, value):
        self.file_port = value

    def get_file_port(self):
        return self.file_port


conf = ReadConfig()
conf.get_config()
