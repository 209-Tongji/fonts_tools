# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 10:53:50 2018

@author: Administrator
"""
import cv2 as cv
import numpy as np

def VThin(image, array,image_x,image_y):
    h = image.shape[1]
    w = image.shape[0]
    NEXT = 1
    for i in range(image_x):
        for j in range(image_y):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i, j - 1] + image[i, j] + image[i, j + 1] if 0 < j < w - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image


def HThin(image, array,image_x,image_y):
    h = image.shape[1]
    w = image.shape[0]
    NEXT = 1
    for j in range(image_x):
        for i in range(image_y):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i - 1, j] + image[i, j] + image[i + 1, j] if 0 < i < h - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and image[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    image[i, j] = array[sum] * 255
                    if array[sum] == 1:
                        NEXT = 0
    return image

def Xihua(image, array, num=10):
    h = image.shape[1]
    w = image.shape[0]
    iXihua = np.zeros((w, h, 1), dtype=np.uint8)
    np.copyto(iXihua, image)
    for i in range(num):
        VThin(iXihua, array,image_x,image_y)
        HThin(iXihua, array,image_x,image_y)
    return iXihua

def Two(image,image_x,image_y):
    h = image.shape[1]
    w = image.shape[0]

    iTwo = np.zeros((w, h, 1), dtype=np.uint8)
    for i in range(image_x):
        for j in range(image_y):
            iTwo[i, j] = 0 if image[i, j] < 200 else 255
    return iTwo
array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, \
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, \
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, \
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, \
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
image = cv.imread('./2021.jpg', 0)
image_x=image.shape[1]
image_y=image.shape[0]
iTwo = Two(image,image_x,image_y)
iThin = Xihua(iTwo, array)
#cv.imshow('image', image)
#cv.imshow('iTwo', iTwo)
#cv.imshow('iThin', iThin)
#cv.waitKey(0)
cv.imwrite('./2021.jpg',iThin)

