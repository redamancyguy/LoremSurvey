import time
import jwt

key = '123456'
username = 'sundassdasdasdaddasdsadwenli'
payload = {'username': username}
data = jwt.encode(payload, key, algorithm='HS256')

print('data:',data)
data2 = jwt.decode(data, '123456', algorithms='HS256')
print(data2)

ss = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InN1bndlbmxpIn0.HSVT1-cXb3xh1f73jeNamGB2i_3BNylB9owYqC1rVUM'

print(len(ss))