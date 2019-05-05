import socket


ip_port = ('103.46.128.43', 33409)
sk = socket.socket()
sk.connect(ip_port)

while True:
    sk.send(b'\xab\xcd')
