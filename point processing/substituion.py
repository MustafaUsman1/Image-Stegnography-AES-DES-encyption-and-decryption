import keygen as kg
import numpy as np
import cv2 as cv

# I = cv.imread('blurry_moon.tif')
I = cv.imread('blurry_moon.tiff')

#read img blurry_moon.tiff
I = cv.imread('blurry_moon.tif')


img = bytearray(I)
#convert byte array to image
I2 = np.array(img)

for index, values in enumerate(img):
    img[index] = values ^ 50
   



#construct a new image from the byte array I2
I3 = I2.reshape(I.shape[0], I.shape[1], I.shape[2])
cv.imwrite('blurry_moon_encrypted.tif', I3)