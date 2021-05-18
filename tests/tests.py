import jwt

key = 'LoremSurvey'
payload = {'username': "sunwenli"}
token = jwt.encode(payload, key, algorithm='HS256')
print(token)
data2 = jwt.decode(token, key, algorithms='HS256')
print(data2)