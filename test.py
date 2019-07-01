import requests
from Util.CommonMethod import *

host = 'http://122.152.228.70:8080/vehicle/interface/login/anon/captcha'

r = requests.get(host)
print(r.text.encode('utf-8'))


with open('test.jpg', 'wb') as f:
    f.write(r.text.encode('utf-8'))
