import socket
client = socket.socket()

client.connect(('103.46.128.43', 33409))
client.send(bytes.fromhex('7E0102037E'))
import time
time.sleep(3)
client.close()