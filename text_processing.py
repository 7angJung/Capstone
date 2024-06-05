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
# 한국어 맞춤법 교정기
get_ipython().system('pip install py-hanspell')


# In[2]:


import torch
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
from spellchecker import SpellChecker
from hanspell import spell_checker
import wordninja

def text_detection(img_path):
    print("2-1 이미지 내 텍스트 인식을 진행 중입니다.")
    # easyocr Reader 생성 (한국어 인식을 위해 'ko' 설정)
    reader = easyocr.Reader(['en','ko'], gpu=False)

    # 이미지 읽기
    img = cv2.imread(img_path)
    height, width, _ = img.shape

    # 페이지를 나누기 위해 이미지의 중간 지점을 계산
    mid_point = width // 2

    # 왼쪽과 오른쪽 페이지 이미지로 나누기
    left_page = img[:, :mid_point]
    right_page = img[:, mid_point:]

    # 텍스트를 저장할 리스트 초기화
    recognized_texts = []

    # 왼쪽 페이지에서 텍스트 인식 및 바운드 박스 그리기
    result_left = reader.readtext(left_page, detail=1)
    for (bbox, text, prob) in result_left:
        # 인식된 텍스트를 리스트에 추가
        if text != 'logi' and text != 'log':
            recognized_texts.append(text)
        # 바운드 박스 좌표 추출 및 그리기
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        cv2.rectangle(left_page, top_left, bottom_right, (0, 255, 0), 2)
        
        # 이미지에 텍스트와 신뢰도 그리기 (PIL 사용)
        img_pil = Image.fromarray(left_page)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("fonts/gulim.ttc", 10)
        text_to_display = f"{text} [{prob:.2f}]"
        draw.text((top_left[0], top_left[1] - 30), text_to_display, font=font, fill=(255,0,0))
        left_page = np.array(img_pil)

    # 오른쪽 페이지에서 텍스트 인식 및 바운드 박스 그리기
    result_right = reader.readtext(right_page, detail=1)
    for (bbox, text, prob) in result_right:
        # 인식된 텍스트를 리스트에 추가
        if text != 'logi' and text != 'log':
            recognized_texts.append(text)
        # 바운드 박스 좌표 추출 및 그리기
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        cv2.rectangle(right_page, top_left, bottom_right, (0, 255, 0), 2)
        
        # 이미지에 텍스트와 신뢰도 그리기 (PIL 사용)
        img_pil = Image.fromarray(right_page)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("fonts/gulim.ttc", 10)
        text_to_display = f"{text} [{prob:.2f}]"
        draw.text((top_left[0], top_left[1] - 30), text_to_display, font=font, fill=(255,0,0))
        right_page = np.array(img_pil)

    # 왼쪽과 오른쪽 페이지를 하나의 이미지로 합치기
    combined_img = np.hstack((left_page, right_page))

    print("2-2 이미지 내 텍스트 인식을 완료했습니다.")
    
    # 이미지 저장 및 표시
    modified_img_path = img_path.replace(".jpg", "_labeled.jpg")  # 수정된 이미지 저장 경로
    cv2.imwrite(modified_img_path, combined_img)
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(combined_img, cv2.COLOR_BGR2RGB))
    plt.title("Image with Bounding Boxes")
    plt.axis('off')
    plt.show()
    print("2-3 이미지 내 텍스트 라벨링 및 저장을 완료했습니다.")

    return recognized_texts, modified_img_path
    
def text_correction(texts):
    # wordninja와 SpellChecker를 이용한 띄어쓰기 및 철자 교정 함수
    print("2-4 텍스트 철자 및 문법 교정을 진행 중입니다. ")

    
    # text가 한글인지 검사
    def is_korean(text):
        for char in text:
            if '\uac00' <= char <= '\ud7a3':
                return True
        return False

    # text가 영어인지 검사
    def is_english(text):
        try:
            text.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    # text가 영어와 한글이 섞여 있는지 검사
    def is_mixed(text):
        return is_english(text) and is_korean(text)
    
    def correct_text(text):
        if is_english(text):
            words = wordninja.split(text)
            spell = SpellChecker()
            corrected_words = [spell.correction(word) for word in words]
            return ' '.join(corrected_words)
        elif is_korean(text):
            print("한글은 아직 정의되지 않았습니다.")
            return text
        elif is_mixed(text):
            return ''
        else:
            print("지원하지 않는 언어입니다.")
            return text
            
    # 입력 데이터가 리스트인 경우
    if isinstance(texts, list):
        corrected_texts = [correct_text(text) for text in texts]
        print("2-5 철자 및 문법 교정을 완료했습니다.")
        return corrected_texts
        
    # 입력 데이터가 문자열인 경우
    elif isinstance(texts, str):
        print("2-5 철자 및 문법 교정을 완료했습니다.")
        return correct_text(texts)
    else:
        raise ValueError("[Error] 입력 데이터는 문자열 또는 리스트여야 합니다.")


# In[ ]:




