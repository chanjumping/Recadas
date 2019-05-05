# !/usr/bin/env python
# --coding:utf-8--
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse
from Util.Log import logger
from Util.CommonMethod import get_md5

curdir = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(curdir, 'root')
media_dir = 'Alarm_Media'
sep = '/'


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_http_request()

    def do_POST(self):
        device_id = self.headers['device']
        alarm_time = self.headers['time']
        authorization = self.headers['Authorization']
        logger.debug('———————————————— 上传附件信息 ————————————————')
        logger.debug('设备ID {}'.format(device_id))
        logger.debug('告警时间 {}'.format(alarm_time))
        logger.debug('认证码 {}'.format(authorization))
        if authorization == get_md5(device_id + get_md5('1CwO4BTUlSi3GuTw') + alarm_time):
            logger.debug('———————————————— 认证码正确 ————————————————')
            boundary = self.headers['Content-Type'].split('=')[1]
            datas = self.rfile.read(int(self.headers['content-length']))
            data_list = datas.split(('--' + boundary).encode('utf-8'))
            media = data_list[1].split(b'\r\n\r\n')[-1].rstrip(b'\r\n')
            up_media_name = data_list[2].split(b'\r\n\r\n')[-1].rstrip(b'\r\n').decode('utf-8')
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)
            with open(os.path.join(media_dir, up_media_name), 'wb') as f:
                f.write(media)
                logger.debug('———————————————— {} 已存储 ————————————————'.format(up_media_name))
        else:
            logger.debug('———————————————— 认证码错误 ————————————————')
        self.handle_http_request()

    def handle_http_request(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        if filepath.endswith('/'):
            filepath += 'index.html'
        if filepath.endswith(".html"):
            mimetype = 'text/html'
            sendReply = True
        if filepath.endswith(".jpg"):
            mimetype = 'image/jpg'
            sendReply = True
        if filepath.endswith(".gif"):
            mimetype = 'image/gif'
            sendReply = True
        if filepath.endswith(".js"):
            mimetype = 'application/javascript'
            sendReply = True
        if filepath.endswith(".css"):
            mimetype = 'text/css'
            sendReply = True
        if filepath.endswith(".json"):
            mimetype = 'application/json'
            sendReply = True
        if filepath.endswith(".woff"):
            mimetype = 'application/x-font-woff'
            sendReply = True
        if sendReply == True:
            try:
                with open(os.path.realpath(root + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


def run_http_server():
    addr = '192.168.100.100'
    port = 9090

    server_address = (addr, port)
    logger.debug('Starting HTTP Server ... IP {} Port {}'.format(addr, port))

    httpd = HTTPServer(server_address, WebServer)
    httpd.serve_forever()


if __name__ == '__main__':
    run_http_server()