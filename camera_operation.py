#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 이미지 영상 처리
get_ipython().system('pip install opencv-python')


# In[1]:


import cv2
import time

def taking_picture():
    # 기본 img_path 값을 설정. 이미지 저장에 실패할 경우 반환할 값입니다.
    img_path = None
    camera = cv2.VideoCapture(2)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("\nTaking picture...")
    ret, frame = camera.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        img_path = f"C:\\Users\\peter\\capstone\\camera\\{timestamp}.jpg"
        cv2.imwrite(img_path, frame)
        print(f"Picture Path : {img_path}\n")
    return img_path

