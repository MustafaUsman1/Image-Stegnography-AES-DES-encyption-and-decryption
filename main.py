from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2 as cv
from random import randint
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Crypto.Cipher import AES
from secrets import token_bytes
from tkinter import messagebox
import os
r=Tk()
r.geometry("500x500")
r.title("Image Encryption and Decryption")

def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]
    return p

def encryptXOR():
    
    file = filedialog.askopenfile(mode = 'r', filetype=[('png files', '*.png'), ('jpg files', '*.jpg'), ('jpeg files', '*.jpeg')])
    if file is not None:
        file=file.name
        I = cv.imread(file)
        #cv.imshow('image', I)
        cv.waitKey(0)

        
    #LSB - Steganography
    bin_data = ""
    for value in I:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]
    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    print(readable_data[:-2])

    #XOR encryption
    img = bytearray(I)
    I2 = np.array(img)
    #loop over the image
    # for index, values in enumerate(img):
    #     I2[index] = values ^ 255
    keyy=[20,55,97,154,210,255,5,96,45,3,132]
    print("Key for XOR operation:")
    print(keyy)
    # Entry1.insert(INSERT, key)
    # Entry1.insert(key)
    for index, values in enumerate(img): 
        I2[index] = values ^ int(keyy[index%6])
        #I2[index] = values ^ int(randint(0,256)%6)
    #construct a new image from the byte array I2
    I3 = I2.reshape(I.shape[0], I.shape[1], I.shape[2])
    # cv.imshow('XOR encryption', I3)
    cv.imwrite('PPencrypted.png', I3 )
    #create file for key    
    f = open("key.txt", "w")
    f.write(str(keyy))
    f.close()


    #XOR decryption
    V = I3
    img = bytearray(V)
    I5 = np.array(img)

    #loop over the image
    # for index, values in enumerate(img):
    #     I2[index] = values ^ 255


    for index, values in enumerate(img):
        I5[index] = values ^ int(keyy[index%6])
   

    #construct a new image from the byte array I2

    I3 = I5.reshape(I.shape[0], I.shape[1], I.shape[2])
    # cv.imshow('XOR decryption', I3)
    cv.imwrite('PPdecoded.png', I3 )


    #histogram
    # hist = cv.calcHist([I],[0],None,[256],[0,256])
    # cv.imshow(hist)
    # plt.hist(img.ravel(),256,[0,256])
    # plt.show()


    #AES encryption
    key = token_bytes(16)
    data = I.tobytes()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce # 16 byt
    ciphertext, tag = cipher.encrypt_and_digest(data) #tag
    f = open("AESencrypted.txt", "wb")
    f.write(nonce)
    f.write(ciphertext)
    f.write(tag)
    f.close()
    pp = bytearray(ciphertext)
    I4 = np.array(pp)
    #convert byte array to image
    #construct a new image from the byte array I2
    I5 = I4.reshape(I.shape[0], I.shape[1], I.shape[2])
    cv.imwrite('AESencrypted.png', I5)

    #AES decryption
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    pp = bytearray(plaintext)
    I6 = np.array(pp)
    #convert byte array to image
    #construct a new image from the byte array I2
    I7 = I6.reshape(I.shape[0], I.shape[1], I.shape[2])
    cv.imwrite('AESdencrypted.png', I7)
    print("AES key:")
    print(key)

    
    
    
    #plotting
    fig = plt.figure("XOR encryption")
    ax = fig.add_subplot(2, 3, 1)
    imgplot = plt.imshow(I)
    ax.set_title('Original image')
    ax = fig.add_subplot(2, 3, 2)
    imgplot = plt.imshow(V)
    ax.set_title('XOR encrypted')
    ax = fig.add_subplot(2, 3, 3)
    imgplot = plt.imshow(I3)
    ax.set_title('XOR decrypted')
    ax = fig.add_subplot(2, 3, 4)
    imgplot = plt.hist(I.ravel(),256,[0,256])
    ax = fig.add_subplot(2, 3, 5)
    imgplot = plt.hist(V.ravel(),256,[0,256])
    ax = fig.add_subplot(2, 3, 6)
    imgplot = plt.hist(I3.ravel(),256,[0,256])

    gig = plt.figure("AES encryption")
    ac = gig.add_subplot(2, 3, 1)
    imgplot = plt.imshow(I)
    ac.set_title('Original image')
    ac = gig.add_subplot(2, 3, 2)
    imgplot = plt.imshow(I5)
    ac.set_title('AES encrypted')
    ac = gig.add_subplot(2, 3, 3)
    imgplot = plt.imshow(I7)
    ac.set_title('AES decrypted')
    ac = gig.add_subplot(2, 3, 4)
    imgplot = plt.hist(I.ravel(),256,[0,256])
    ac = gig.add_subplot(2, 3, 5)
    imgplot = plt.hist(I5.ravel(),256,[0,256])
    ac = gig.add_subplot(2, 3, 6)
    imgplot = plt.hist(I7.ravel(),256,[0,256])
    plt.show()

    
    messagebox.showinfo("Secret embedded Message", readable_data[:-2])
    mylabel.config(text="Secret Message: " + readable_data[:-2])
    messagebox.showinfo("AES key", str(key))
    # mylabel.config(text="AES key: " + key)
    #add aes key to lable l1
    l1.config(text="AES key: " + str(key))

    messagebox.showinfo("XOR key", keyy)
    l2.config(text="XOR key: " + str(keyy))

    #get image size
    size = os.path.getsize(file)
    # messagebox.showinfo("Orignal Image size in bytes", size)
    l3.config(text="Orignal Image size in bytes: " + str(size))

    size = os.path.getsize('AESencrypted.png')
    # messagebox.showinfo("AES encrypted Image size in bytes", size)
    l4.config(text="AES encrypted Image size in bytes: " + str(size))

    size = os.path.getsize('PPencrypted.png')
    # messagebox.showinfo("XOR decrypted Image size in bytes", size)
    l5.config(text="XOR encrypted Image size in bytes: " + str(size))

    size = os.path.getsize('AESdencrypted.png')
    # messagebox.showinfo("AES decrypted Image size in bytes", size)
    l6.config(text="AES decrypted Image size in bytes: " + str(size))

    size = os.path.getsize('PPdecoded.png')
    # messagebox.showinfo("XOR decrypted Image size in bytes", size)
    l7.config(text="XOR decrypted Image size in bytes: " + str(size))



mylabel=Label(r,text="")
mylabel.place(x=100,y=50)

#create label
l1=Label(r,text="")
l1.place(x=100,y=100)


#create label
l2=Label(r,text="")
l2.place(x=100,y=150)

#create label
l3=Label(r,text="")
l3.place(x=100,y=200)

#create label
l4=Label(r,text="")
l4.place(x=100,y=250)

#create label
l5=Label(r,text="")
l5.place(x=100,y=300)

#create label
l6=Label(r,text="")
l6.place(x=100,y=350)

#create label
l7=Label(r,text="")
l7.place(x=100,y=400)



b1=Button(r,text="Finished",command=encryptXOR())
b1.place(x=200,y=450)





r.mainloop()
