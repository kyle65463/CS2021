#!/usr/bin/env python3
import cv2      #https://pypi.org/project/opencv-python/

def encrypt(img1, img2):
    h, w = img1.shape
    for i in range(h):
        for j in range(w):
            img1[i][j] ^= img2[i][j]

msg1 = cv2.imread('flag_enc.png', cv2.IMREAD_GRAYSCALE)
msg2 = cv2.imread('golem_enc.png', cv2.IMREAD_GRAYSCALE)
encrypt(msg1, msg2)
cv2.imwrite('flag.png', msg1)