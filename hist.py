import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('AESdencrypted.png',0)
hist = cv2.calcHist([img],[0],None,[256],[0,256])
cv2.imshow(hist)
plt.hist(img.ravel(),256,[0,256])
plt.show()


