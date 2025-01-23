#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# PyTorch와 torchvision 설치
get_ipython().system('pip install torch torchvision torchaudio')
# 데이터를 분석 및 조작
get_ipython().system('pip install pandas')
# 이미지 작업
get_ipython().system('pip install pillow')
# matplotlib 설치
get_ipython().system('pip install matplotlib')
# GUI 없는 환경에서 OpenCV 사용을 위해
get_ipython().system('pip install opencv-python-headless')
# clone
get_ipython().system('git clone https://github.com/ultralytics/yolov5')


# In[1]:


import torch
import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys

def crop_image(image_path):
    # 모델 로드
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")

    # 추론 수행
    results = model(image_path)

    # detected된 모든 객체를 pandas 데이터프레임 형태로 변환
    df = results.pandas().xyxy[0]

    # 'book' 클래스의 객체들만 필터링
    book_df = df[df['name'] == 'book']

    if not book_df.empty:
        highest_conf_row = book_df.loc[book_df['confidence'].idxmax()]

        # 이미지 로드
        img = Image.open(image_path)

        # 이미지 저장 전 파일명 수정
        img_filename = os.path.splitext(os.path.basename(image_path))[0]
        base_path = "C:\\Users\\peter\\capstone\\onePage\\"
        
        # 바운딩 박스로 이미지 자르기
        cropped = img.crop((int(highest_conf_row['xmin']), int(highest_conf_row['ymin']), int(highest_conf_row['xmax']), int(highest_conf_row['ymax'])))
        
        # 책인지 단순 문서인지 구분
        width, height = cropped.size  # 자른 이미지의 너비와 높이 가져오기
        ratio = height / width

        if 1.2 < ratio < 1.7:
            # 문서일 경우, 이미지를 나누지 않고 저장
            print(f"\n해당 이미지 내에 객체는 문서이거나, 책의 한쪽 페이지입니다.")
            cropped_image_path = f"{base_path}{img_filename}_cropped.jpg"
            cropped.save(cropped_image_path)
            left_half_path = ""
            right_half_path = ""
            print(f"\n이미지를 {cropped_image_path}로 자르고 저장했습니다.")
        else:
            # 문서가 아닐 경우, 이미지를 가로로 반으로 나누기
            cropped_image_path = image_path.replace(".jpg", "_cropped.jpg")
            cropped.save(cropped_image_path)
            left_half = cropped.crop((0, 0, width/2, height))
            right_half = cropped.crop((width/2, 0, width, height))
            
            # 나눠진 이미지 파일 경로 설정
            cropped_image_path = ""
            left_half_path = f"{base_path}{img_filename}_left.jpg"
            right_half_path = f"{base_path}{img_filename}_right.jpg"
            
            # 나눠진 이미지 파일 저장
            left_half.save(left_half_path)
            right_half.save(right_half_path)
            print(f"\n이미지를 {cropped_image_path}, {left_half_path}, {right_half_path}로 자르고 저장했습니다.")
        
        return cropped_image_path, left_half_path, right_half_path

    else:
        print("\n탐지된 'book'이 없습니다.")
        return None, None, None  # 'book'이 탐지되지 않음


# In[ ]:




