import numpy as np
a = np.array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11],
       [12, 13, 14, 15]])
list = [i for i in range(len(a[0]))]
list1 = [(len(a)-i-1) for i in range(len(a[0]))]
print(list)
print(list1)
a[:,list]=a[:,list1]

print(a)