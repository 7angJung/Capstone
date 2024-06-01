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


# In[20]:


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
    print("이미지 내 텍스트 인식을 진행 중입니다...")
    # easyocr Reader 생성 (한국어와 영어 인식을 위해 'ko'와 'en' 설정)
    reader = easyocr.Reader(['ko', 'en'], gpu=False)

    # 이미지 읽기
    img = cv2.imread(img_path)

    # 텍스트를 저장할 리스트 초기화
    recognized_texts = []

    # 이미지에서 텍스트 인식 및 바운드 박스 그리기
    result = reader.readtext(img, detail=1)
    for (bbox, text, prob) in result:
        # 인식된 텍스트를 리스트에 추가
        if text != 'logi' and text != 'log':
            recognized_texts.append(text)
        # 바운드 박스 좌표 추출 및 그리기
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        
        # 이미지에 텍스트와 신뢰도 그리기 (PIL 사용)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("fonts/gulim.ttc", 10)
        text_to_display = f"{text} [{prob:.2f}]"
        draw.text((top_left[0], top_left[1] - 30), text_to_display, font=font, fill=(255,0,0))
        img = np.array(img_pil)

    print("이미지 내 텍스트 인식을 완료했습니다.")
    
    # 이미지 저장 및 표시
    modified_img_path = img_path.replace(".jpg", "_labeled.jpg")  # 수정된 이미지 저장 경로
    cv2.imwrite(modified_img_path, img)
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Image with Bounding Boxes")
    plt.axis('off')
    plt.show()
    print("이미지 내 텍스트 라벨링을 완료했습니다.")
    
    # 인식된 텍스트 리스트를 반환
    return recognized_texts
    
def text_correction(texts):
    # wordninja와 SpellChecker를 이용한 띄어쓰기 및 철자 교정 함수
    print("텍스트 철자 및 문법 교정을 진행 중입니다...")
    def correct_text(text):
        words = wordninja.split(text)
        spell = SpellChecker()
        corrected_words = [spell.correction(word) for word in words]
        return ' '.join(corrected_words)
        
    # 입력 데이터가 리스트인 경우
    if isinstance(texts, list):
        corrected_texts = [correct_text(text) for text in texts]
        print("철자 및 문법 교정을 완료했습니다.")
        return corrected_texts
    # 입력 데이터가 문자열인 경우
    elif isinstance(texts, str):
        return correct_text(texts)
    else:
        raise ValueError("입력 데이터는 문자열 또는 리스트여야 합니다.")


# In[21]:


import cv2
import time
import os
import easyocr

# 비디오 캡처 설정
video = cv2.VideoCapture(2)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = video.read()
if ret:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    img_path = f"C:\\Users\\peter\\capstone\\camera\\{timestamp}.jpg"
    cv2.imwrite(img_path, frame)
    print(f"Picture Path : {img_path}\n")

    texts = text_detection(img_path)
    print(texts)


# In[13]:


import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# T5 모델 및 토크나이저 로드
model_name = "digit82/kolang-t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def text_correction(texts):
    print("텍스트 철자 및 문법 교정을 진행 중입니다...")

    # 텍스트 교정 함수
    def correct_text(text):
        input_text = "맞춤법을 고쳐주세요: " + text
        input_encoding = tokenizer(input_text, return_tensors="pt")
        
        input_ids = input_encoding.input_ids.to(device)
        attention_mask = input_encoding.attention_mask.to(device)

        # T5 모델로부터 출력 생성
        output_encoding = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=128,
            num_beams=5,
            early_stopping=True,
        )

        # 출력 문장 디코딩
        corrected_text = tokenizer.decode(output_encoding[0], skip_special_tokens=True)
        return corrected_text

    # 입력 데이터가 리스트인 경우
    if isinstance(texts, list):
        corrected_texts = [correct_text(text) for text in texts]
    # 입력 데이터가 문자열인 경우
    elif isinstance(texts, str):
        corrected_texts = correct_text(texts)
    else:
        raise ValueError("입력 데이터는 문자열 또는 리스트여야 합니다.")

    print("철자 및 문법 교정을 완료했습니다.")
    return corrected_texts

test = ['아부지를 만나구 싶디','where are yo from','내 이루믄 정광혁이야']
print(text_correction(test))


# In[17]:


def text_correction(texts):
    # wordninja와 SpellChecker를 이용한 띄어쓰기 및 철자 교정 함수
    print("텍스트 철자 및 문법 교정을 진행 중입니다...")
    def correct_text(text):
        words = wordninja.split(text)
        spell = SpellChecker()
        corrected_words = [spell.correction(word) for word in words]
        return ' '.join(corrected_words)
        
    # 입력 데이터가 리스트인 경우
    if isinstance(texts, list):
        corrected_texts = [correct_text(text) for text in texts]
        print("철자 및 문법 교정을 완료했습니다.")
        return corrected_texts
    # 입력 데이터가 문자열인 경우
    elif isinstance(texts, str):
        return correct_text(texts)
    else:
        raise ValueError("입력 데이터는 문자열 또는 리스트여야 합니다.")

texts = ['Imthequeenofmars','어떻게하면좋을까','letsgetonwithit','howboutthat']

print(text_correction(texts))


# In[ ]:


def text_detection(img_path):
    print("이미지 내 텍스트 인식을 진행 중입니다...")
    # easyocr Reader 생성 (한국어와 영어 인식을 위해 'ko'와 'en' 설정)
    reader = easyocr.Reader(['ko', 'en'], gpu=False)

    # 이미지 읽기
    img = cv2.imread(img_path)

    # 텍스트를 저장할 리스트 초기화
    recognized_texts = []

    # 이미지에서 텍스트 인식 및 바운드 박스 그리기
    result = reader.readtext(img, detail=1)
    for (bbox, text, prob) in result:
        # 인식된 텍스트를 리스트에 추가
        recognized_texts.append(text)
        # 바운드 박스 좌표 추출 및 그리기
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        
        # 이미지에 텍스트와 신뢰도 그리기 (PIL 사용)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("fonts/gulim.ttc", 20)
        text_to_display = f"{text} [{prob:.2f}]"
        draw.text((top_left[0], top_left[1] - 30), text_to_display, font=font, fill=(255,0,0))
        img = np.array(img_pil)

    print("이미지 내 텍스트 인식을 완료했습니다.")
    
    # 이미지 저장 및 표시
    modified_img_path = img_path.replace(".jpg", "_labeled.jpg")  # 수정된 이미지 저장 경로
    cv2.imwrite(modified_img_path, img)
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Image with Bounding Boxes")
    plt.axis('off')
    plt.show()
    print("이미지 내 텍스트 라벨링을 완료했습니다.")
    
    # 인식된 텍스트 리스트를 반환
    return recognized_texts

