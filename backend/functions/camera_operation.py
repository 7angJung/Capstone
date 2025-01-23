#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 이미지 영상 처리
get_ipython().system('pip install opencv-python')


# In[1]:


import cv2
import time

def taking_picture(camera):
    # 기본 img_path 값을 설정. 이미지 저장에 실패할 경우 반환할 값입니다.
    img_path = None
    print("1-1 이미지 촬영 진행 중입니다.")
    ret, frame = camera.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        img_path = f"C:\\Users\\peter\\capstone\\camera\\{timestamp}.jpg"
        cv2.imwrite(img_path, frame)
        print("1-2 이미지 촬영이 완료되었습니다.")
        print(f"이미지 경로 : {img_path}\n")
        return img_path
    else:
        print("[Error] 이미지 촬영에 실패했습니다. 카메라 연결을 확인해 주세요")
        return None

