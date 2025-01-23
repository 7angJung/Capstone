# 실시간 점자 변환 시스템

시각장애인은 주로 음성 합성 기술을 통해 정보를 얻지만, 발음이 유사한 단어를 듣는 경우 이해에 어려움을 느낀다. 이 연구는 이런 어려움 해결을 위해 책이나 문서를 쉽게 점자로 변환 할 수 있는 시스템을 제안한다. 제안한 시스템은 책 이미지를 점자정보로 만드는 점자번역기와 점자정보를 물리적인 점자로 생성하는 점자변환기로 구성되고, 점자변환기의 점자 표현은 자체 개발한 점자 모듈인 ‘쩜구’를 사용한다. 개발한 점자변환기는 점자 도서관장의 긍정적인 평가를 받았으며, 실제 시각장애인의 독서 경험을 향상시킬 것으로 기대한다.

## Package
```bash
.
├─backend
│  ├─functions
│  └─server
├─database
│  ├─braille picture
│  └─user picture
├─frontend
│  └─templates
└─static
``` 
    
## Environment
- **Python 3.8**
- **Libraries**
    - easyocr
    - opencv-python
    - numpy
    - flask
    - pillow
    - pyserial
      
## Stack
- **Frontend**
    - HTML
    - CSS
    - JavaScript
- **Backend**
    - Python (Flask)
- **Hardware**
    - Webcam
    - Arduino Mega
    - Servo

## Structure
![git_readme_image-001](https://github.com/user-attachments/assets/161b5fee-1b16-4bc1-9719-64adee64a5a5)
