
import numpy as np
import cv2 as cv
from random import randint

I = cv.imread('blurry_moon.tif')

def encrypt(I):
    
    img = bytearray(I)
    I2 = np.array(img)

    #loop over the image
    # for index, values in enumerate(img):
    #     I2[index] = values ^ 255

    key=[20,55,97,154,210,255]
    for index, values in enumerate(img):
        
        I2[index] = values ^ int(key[index%6])
        #I2[index] = values ^ int(randint(0,256)%6)

    #construct a new image from the byte array I2

    I3 = I2.reshape(I.shape[0], I.shape[1], I.shape[2])
    cv.imwrite('PPencrypted.png', I3 )
    #create file for key    
    f = open("key.txt", "w")
    f.write(str(key))
    f.close()


V = cv.imread('PPencrypted.png')
def decrypt(V, key):
    
    img = bytearray(V)
    I5 = np.array(img)

    #loop over the image
    # for index, values in enumerate(img):
    #     I2[index] = values ^ 255


    for index, values in enumerate(img):
        I5[index] = values ^ int(key[index%6])
   

    #construct a new image from the byte array I2

    I3 = I5.reshape(I.shape[0], I.shape[1], I.shape[2])
    cv.imwrite('PPdecoded.png', I3 )

encrypt(I)
decrypt(V, [20,55,97,154,210,255])