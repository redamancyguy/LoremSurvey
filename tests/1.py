import sys

import cv2
import numpy as np
img = cv2.imread('1.png',1)

cv2.namedWindow('Image')
mat=np.array(img)

d = np.array_split(mat, 3, axis=2)  # array split允许指定沿哪个轴分割。同vsplit
print(d)
print(len(d))

for i in d:
    print(type(i))
    print(i.shape)
    i[:,[ii for ii in range(len(i[0]))]]=i[:,[(len(i[0])-ii-1) for ii in range(len(i[0]))]]
    i = i.T
    cv2.imshow("m1", i[0])
# cv2.imshow("m1", np.array(d[:][0]))
print(np.array(d[:][:][0]).shape)
cv2.waitKey(2000)
sys.exit()
