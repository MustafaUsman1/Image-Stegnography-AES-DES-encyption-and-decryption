


import cv2 as cv
import numpy as np
from random import randint
I = cv.imread('street_noisy.png')
img = bytearray(I)

h=I.shape[0]
w=I.shape[1]
e=np.zeros(shape=[w,h], dtype=np.uint8)


def shuffle(img, index, x, y):
    e=img
    for i in range(x):
        k=1
        for j in range(y):
            a=index[i%10] #
            e[i][j] = img[i][a]
            k=k+1
    return e

kk=img
key = [128,65,0,255,45,63,2,50,155,69]
print(key)
e = shuffle(I, key, w, h)

e = shuffle(e, key, h, w)
#creat a file for I
cv.imwrite('blurry_moon_dencrypted.jpg', e )
