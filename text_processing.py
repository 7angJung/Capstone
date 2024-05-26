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


# In[1]:


"""
import torch
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
from spellchecker import SpellChecker
import wordninja

global recognized_texts_global = []
global current_text_index = 0

def text_detection(left_img_path, right_img_path):
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
    recognize_text_and_draw_bbox(left_img, 'C:\\Users\\peter\\capstone\\boundingBox\\left_half.jpg', "Left Page with Bounding Boxes")
    recognize_text_and_draw_bbox(right_img, 'C:\\Users\\peter\\capstone\\boundingBox\\right_half.jpg', "Right Page with Bounding Boxes")

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
        
def detect_text_in_picture(img_path):
    global recognized_texts_global
    global current_text_index
    print("detecting text in picture...")
    crop_book(img_path)
    img_left = "C:\\Users\\peter\\capstone\\onePage\\left_half.jpg"
    img_right = "C:\\Users\\peter\\capstone\\onePage\\right_half.jpg"
    recognized_texts = text_detection(img_left, img_right)
    print("[인식된 텍스트]")
    print(recognized_texts)
    words_list = [word for text in recognized_texts for word in text.split()]
    corrected_texts = text_correction(words_list)
    filtered_texts = [text for text in corrected_texts if text.strip()]
    print(filtered_texts)
    recognized_texts_global = filtered_texts
    current_text_index = 0
"""


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

