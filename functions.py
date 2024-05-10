#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# OCR 모델
get_ipython().system('pip install easyocr')
# 이미지 영상 처리
get_ipython().system('pip install opencv-python')
# PyTorch와 torchvision 설치
get_ipython().system('pip install torch torchvision torchaudio')
# matplotlib 설치
get_ipython().system('pip install matplotlib')
# GUI 없는 환경에서 OpenCV 사용을 위해
get_ipython().system('pip install opencv-python-headless')
# clone
get_ipython().system('git clone https://github.com/ultralytics/yolov5')


# In[2]:


import torch
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def detect_objects(image_path):
    """
    객체 탐지 함수
    
    Parameters:
    image_path (str): 탐지할 이미지의 경로
    """
    # 모델 불러오기
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # 다양한 모델 옵션 사용 가능: yolov5n - yolov5x6, custom
    
    # 이미지
    img = image_path  # or file, Path, PIL, OpenCV, numpy, list
    
    # 추론
    results = model(img)
    
    # 결과 출력
    results.print()  # 다른 옵션: .show(), .save(), .crop(), .pandas() 등
    
    # 결과 이미지 보여주기
    results.show()

def crop_book(image_path, left_half_path='C:\\Users\\peter\\capstone\\onePage\\left_half.jpg', right_half_path='C:\\Users\\peter\\capstone\\onePage\\right_half.jpg'):
    """
    이미지에서 'book' 객체를 탐지하고 가장 높은 신뢰도를 가진 'book' 객체의 이미지를 가로로 반으로 나누어 저장합니다.

    Args:
    - image_path: 탐지를 수행할 이미지 경로
    - left_half_path: 왼쪽 반쪽 이미지를 저장할 경로
    - right_half_path: 오른쪽 반쪽 이미지를 저장할 경로
    """
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

def text_detection(left_img_path='C:\\Users\\peter\\capstone\\onePage\\left_half.jpg', right_ig_path='C:\\Users\\peter\\capstone\\onePage\\right_half.jpg'):
    # easyocr Reader 생성 (한국어와 영어 인식을 위해 'ko'와 'en' 설정)
    reader = easyocr.Reader(['ko', 'en'], gpu=False)

    # 이미지 읽기
    left_img = cv2.imread(left_img_path)
    right_img = cv2.imread(right_img_path)

    # 텍스트를 저장할 리스트 초기화
    recognized_texts = []

    # 이미지에서 텍스트 인식 및 바운드 박스 그리기 함수 정의
    def recognize_text_and_draw_bbox(image, image_path, title):
        result = reader.readtext(image)
        for (bbox, text, prob) in result:
            # 인식된 텍스트를 리스트에 추가
            recognized_texts.append(text)
            # 바운드 박스 좌표 추출 및 그리기
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # 이미지 저장 및 표시
        cv2.imwrite(image_path, image)
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.show()

    # 왼쪽 및 오른쪽 이미지에 대해 텍스트 인식 및 바운드 박스 그리기 수행
    recognize_text_and_draw_bbox(left_img, 'C:\\Users\\peter\\capstone\\onePage\\left_half.jpg', "Left Page with Bounding Boxes")
    recognize_text_and_draw_bbox(right_img, 'C:\\Users\\peter\\capstone\\onePage\\right_half.jpg', "Right Page with Bounding Boxes")

    # 인식된 텍스트 리스트를 반환
    return recognized_texts


# In[ ]:




