from question.models1 import Mdb

if __name__ == '__main__':
    db = Mdb.getDatabase('test1')
    print(db.test.estimated_document_count())
    print('=========', db.test.insert_one({'test': 'test'}).inserted_id)
    for item in db.test.find({'title': {'$in': ['test', 'test2']}}):
        print(item)
    for item in db.test.find():
        print(item)
    # db.test.drop()
    db.command("dropDatabase")
    # paging
    # for i in range(int((db.test.estimated_document_count()+1)/2)):
    #     print('======================')
    #     for item in db.test.find().limit(2).skip(i*2):
    #         print(item)
