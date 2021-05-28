import pymysql
from question.models1 import M

# 数据库
db = ""
cur = ""
try:
    # 数据库配置
    config = {
        "host": "39.104.209.232",
        "port": 3306,
        "user": "LoremSurvey",
        "password": "12345678900",
        "db": 'LoremSurvey',
        "charset": "utf8mb4",
    }
    db = pymysql.connect(**config)
    # 游标
    cur = db.cursor(pymysql.cursors.DictCursor)
except:
    print("连接数据库失败")
    exit(-1)

cur.execute('SELECT * FROM user_user')
List = cur.fetchall()
mdb = M.getDatabase()
print(List)
mdb.test.insert_many(List)
# db.test.update({},{$unset:{'id':''}},{multi:true})
mdb.test.update_many({}, {'$unset': {'id': ''}})
# mdb.test.removeField('id')
# mdb.command('dropDatabase')
for i in mdb.test.find({}, {'id': 1}):
    print(i['_id'])
cur.close()
db.close()
