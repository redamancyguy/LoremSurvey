import time
def work1():
    for i in range(5):
        print('work1',i)
        yield
        # time.sleep(1)
    return

def work2():
    for i in range(5):
        print('work2',i)
        yield
        # time.sleep(1)
    return

w1 = work1()
w2 = work2()

import sys  # while循环需要带异常处理
while True:
    try:
        next(w1)
        next(w2)
    except StopIteration:
        sys.exit()