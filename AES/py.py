from Crypto.Cipher import AES
from secrets import token_bytes
import cv2
import numpy as np

key = token_bytes(16) # 16 bytes = 128 bits

def encrypt(data):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce # 16 byt
    ciphertext, tag = cipher.encrypt_and_digest(data) #tag
    
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext



#encypting
#read chumi.jpg
img = cv2.imread('blurry_moon.tif')
#convert to bytes
data = img.tobytes()

#encrypt
nonce, ciphertext, tag = encrypt(data)
f = open("encrypted.txt", "wb")
f.write(nonce)
f.write(ciphertext)
f.write(tag)
f.close()

###
pp = bytearray(ciphertext)
I4 = np.array(pp)
#convert byte array to image
#construct a new image from the byte array I2
I5 = I4.reshape(img.shape[0], img.shape[1], img.shape[2])
cv2.imwrite('encrypted.jpg', I5)


# decryption
# decrypt chumi_encrypted.jpg
plaintext = decrypt(nonce, ciphertext, tag)
f = open("dencrypted.txt", "wb")
f.write(plaintext)
f.close()




#convert to bytes
data2 = bytearray(plaintext)

#convert to image
I2 = np.array(data2)
#convert byte array to image
#construct a new image from the byte array I2
I3 = I2.reshape(img.shape[0], img.shape[1], img.shape[2])
cv2.imwrite('dencrypted.jpg', I3)

print(nonce, '\n', tag)