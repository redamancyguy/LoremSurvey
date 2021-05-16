from greenlet import greenlet
import time


def work1():
    for i in range(5):
        print('work1',i)
        g2.switch()   #遇到耗时操作，手动切换其他操作,(现在切换了gg2协程)
        g2.switch()   #遇到耗时操作，手动切换其他操作,(现在切换了gg2协程)

def work2():
    for i in range(5):
        print('work2', i)
        g1.switch()

def work3():
    for i in range(5):
        print('work3', i)
        g3.switch()


# 创建多协程
g1 = greenlet(work1)
g2 = greenlet(work2)
g3 = greenlet(work3)

g1.run

#启动协程
g1.switch()
g2.switch()
g3.switch()



