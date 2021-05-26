from pymongo import MongoClient

if __name__ == '__main__':

    # 建立Mongodb数据库连接
    # client = MongoClient('127.0.0.1', 27017)
    client = MongoClient('39.104.209.232', 27017)
    # test为数据库

    db = client.test
    # test为集合，相当于表名
    db.authenticate('user','123456789')
    collection = db.test
    # 插入集合数据
    collection.insert_one({"title": "test2"})
    # 打印集合中所有数据
    for item in collection.find():
        print(item)
    client.close()
    print(collection.find_one())
    # collection.delete_many('title')
    collection.drop()
