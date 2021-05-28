import redis

db = redis.Redis(host='localhost', port=6379, decode_responses=True)
# print(db.get('name'))
# db.set('name','sunwenli2')
# print(db.get('name'))
db.close()
