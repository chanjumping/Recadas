import requests
from Util.CommonMethod import *

# host = 'http://122.152.228.70:8080/vehicle/interface/login/anon/captcha'
host = 'http://122.152.228.70:8080/vehicle/interface/login/anon/status'

r = requests.get(host)
print(r.text)


# with open('test.jpg', 'wb') as f:
#     f.write(r.text)

with open(r'C:\Users\Administrator\Desktop\git\Recadas\captcha.jpg', 'rb') as f:
    print(f.read())

with open(r'C:\Users\Administrator\Desktop\git\Recadas\Alarm_Media\00218510624_1562039478972_0.jpg', 'rb') as f:
    print(f.read())