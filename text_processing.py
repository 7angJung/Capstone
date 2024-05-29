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
# spellchecker 설치
get_ipython().system('pip install pyspellchecker')
# wordninja 설치
get_ipython().system('pip install wordninja')


# In[ ]:


import torch
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
from spellchecker import SpellChecker
import wordninja

def text_detection(img_path):
    # easyocr Reader 생성 (한국어와 영어 인식을 위해 'ko'와 'en' 설정)
    reader = easyocr.Reader(['ko', 'en'], gpu=False)

    # 이미지 읽기
    img = cv2.imread(img_path)

    # 텍스트를 저장할 리스트 초기화
    recognized_texts = []

    # 이미지에서 텍스트 인식 및 바운드 박스 그리기
    result = reader.readtext(img)
    for (bbox, text, prob) in result:
        # 인식된 텍스트를 리스트에 추가
        recognized_texts.append(text)
        # 바운드 박스 좌표 추출 및 그리기
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

    # 이미지 저장 및 표시
    modified_img_path = img_path.replace(".jpg", "_with_bbox.jpg")  # 수정된 이미지 저장 경로
    cv2.imwrite(modified_img_path, img)
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Image with Bounding Boxes")
    plt.axis('off')
    plt.show()

    # 인식된 텍스트 리스트를 반환
    return recognized_texts
    
def text_correction(texts):
    # wordninja와 SpellChecker를 이용한 띄어쓰기 및 철자 교정 함수
    def correct_text(text):
        words = wordninja.split(text)
        spell = SpellChecker()
        corrected_words = [spell.correction(word) for word in words]
        return ' '.join(corrected_words)

    # 입력 데이터가 리스트인 경우
    if isinstance(texts, list):
        corrected_texts = [correct_text(text) for text in texts]
        return corrected_texts
    # 입력 데이터가 문자열인 경우
    elif isinstance(texts, str):
        return correct_text(texts)
    else:
        raise ValueError("입력 데이터는 문자열 또는 리스트여야 합니다.")

