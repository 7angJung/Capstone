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


"""
import torch
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys

def crop_book(image_path, left_half_path, right_half_path):
    # 모델 로드
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # YOLOv5 모델 버전 선택

    # 추론 수행
    results = model(image_path)

    # detected된 모든 객체를 pandas 데이터프레임 형태로 변환
    df = results.pandas().xyxy[0]

    # 'book' 클래스의 객체들만 필터링
    book_df = df[df['name'] == 'book']

    # confidence가 가장 높은 'book' 객체 찾기
    if not book_df.empty:
        highest_conf_row = book_df.loc[book_df['confidence'].idxmax()]
        
        # 이미지 로드
        img = Image.open(image_path)
        
        # 바운딩 박스로 이미지 자르기
        cropped = img.crop((int(highest_conf_row['xmin']), int(highest_conf_row['ymin']), int(highest_conf_row['xmax']), int(highest_conf_row['ymax'])))
        
        # 이미지를 가로로 반으로 나누기
        width, height = cropped.size
        left_half = cropped.crop((0, 0, width/2, height))
        right_half = cropped.crop((width/2, 0, width, height))
        
        # 나눠진 이미지 파일 저장
        left_half.save(left_half_path)
        right_half.save(right_half_path)
        
        return True  # 성공적으로 처리됨
    else:
        print("탐지된 'book'이 없습니다.")
        return False  # 'book'이 탐지되지 않음
"""


# In[3]:


import torch
import cv2
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
        
        # 바운딩 박스로 이미지 자르기
        cropped = img.crop((int(highest_conf_row['xmin']), int(highest_conf_row['ymin']), int(highest_conf_row['xmax']), int(highest_conf_row['ymax'])))
        
        # 자른 이미지 저장
        cropped_image_path = image_path.replace(".jpg", "_cropped.jpg")
        cropped.save(cropped_image_path)
        print(f"이미지를 {cropped_image_path}로 자르고 저장했습니다.")

        # 이미지를 가로로 반으로 나누기
        width, height = cropped_image_path.size
        left_half = cropped.crop((0, 0, width/2, height))
        right_half = cropped.crop((width/2, 0, width, height))
        
        # 나눠진 이미지 파일 저장
        left_half.save(left_half_path)
        right_half.save(right_half_path)
        
        return True

    else:
        print("탐지된 'book'이 없습니다.")
        return None  # 'book'이 탐지되지 않음
        
# 책인지 단순 문서인지 구분을 위한 함수
def is_document(image_path):
    # 이미지 열기
    with Image.open(image_path) as img:
        width, height = img.size  # 이미지의 너비와 높이 가져오기
        
    # 이미지의 비율 계산
    ratio = height / width
    
    # 비율을 기반으로 문서인지 아닌지 판별
    if 1.2 < ratio < 1.7:
        return True
    else:
        return False

