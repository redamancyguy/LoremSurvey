#第三种：
'''gevent包'''
import gevent
from gevent import monkey  #猴子补丁
monkey.patch_all()     #给所有的耗时操作打上补丁，协程自动切换

import time

def work1():
    for i in range(5):
        print('work1',i)
        time.sleep(1)

def work2():
    for i in range(5):
        print('work2', i)
        time.sleep(1)

#创建多协程与    创建多进程\多线程    的过程差不多
g1 = gevent.spawn(work1)       #创建协程1
g2 = gevent.spawn(work2)      #创建协程2
g1.join()  #等待协程操作完成
g2.join()