#!/usr/bin/env python
# coding: utf-8

# In[17]:


def text_to_braille(text_list):
    braille_dict = {
        # 기본 알파벳 점자
        'a': '01', 'b': '40', 'c': '11', 'd': '14', 'e': '12', 'f': '41', 'g': '44',
        'h': '42', 'i': '21', 'j': '24', 'k': '50', 'l': '70', 'm': '51', 'n': '54',
        'o': '52', 'p': '71', 'q': '74', 'r': '72', 's': '61', 't': '64', 'u': '53',
        'v': '73', 'w': '27', 'x': '55', 'y': '57', 'z': '56',
        
        # 숫자
        '1': '10', '2': '40', '3': '11', '4': '14', '5': '12', 
        '6': '41', '7': '44', '8': '42', '9': '21', '0': '24',
        
        # 기본 부호  
        '.': '02', ',': '26', '?': '63', '!': '62', '“': '63', '”': '36',
        "‘": '0363', "’": '3630', '-': '33', '(': '6330', ')': '0336',
    }
    hangul_initials = {
        # 한글 점자 초성 
        'ㄱ': '01', 'ㄴ': '11', 'ㄷ': '21', 'ㄹ': '02', 'ㅁ': '12', 'ㅂ': '04',
        'ㅅ': '03', 'ㅇ': '66', 'ㅈ': '50', 'ㅊ': '60', 'ㅋ': '62', 'ㅌ': '63',
        'ㅍ': '26', 'ㅎ': '36'
    }
    
    hangul_medials = {
        # 한글 점자 중성 
        'ㅏ': '43', 'ㅑ': '34', 'ㅓ': '61', 'ㅕ': '16', 'ㅗ': '53', 'ㅛ': '35',
        'ㅜ': '51', 'ㅠ': '15', 'ㅡ': '25', 'ㅣ': '52', 'ㅢ': '27', 'ㅔ': '54',
        'ㅐ': '72', 'ㅖ': '31', 'ㅘ': '73', 'ㅝ': '71', 'ㅚ': '57', 'ㅟ': '5172', 
        'ㅒ': '3472', 'ㅙ': '7372', 'ㅞ': '7172'
    }
    
    hangul_finals = {
        # 한글 점자 종성 
        'ㄱ': '10', 'ㄴ': '22', 'ㄷ': '32', 'ㄹ': '20', 'ㅁ': '23', 'ㅂ': '40',
        'ㅅ': '30', 'ㅇ': '66', 'ㅈ': '50', 'ㅊ': '60', 'ㅋ': '62', 'ㅌ': '63',
        'ㅍ': '26', 'ㅎ': '36'
    }
    hangul_abbreviations_syllable = {
        # 한글 점자 음절 약자 
        '가': '45', '나': '11', '다': '21', '마': '12', '바': '04', '사': '70', 
        '자': '05', '카': '41', '타': '42', '파': '14', '하': '24', '억': '17', 
        '언': '67', '얼': '64', '연': '13', '열': '46', '영': '47', '옥': '55',
        '온': '76', '옹': '77', '운': '44', '울': '75', '은': '56', '을': '65', 
        '인': '74', '것': '0761'
    }
    hangul_abbreviations_word = {
        # 한글 점자 단어 약자 
        '그러나': '1011', '그러면': '1022', '그래서': '1061', '그런데': '1054',
        '그러므로': '1023', '그리고': '1053', '그리하여': '1016'
    }
    def is_english(text):
        return all('A' <= char <= 'Z' or 'a' <= char <= 'z' for char in text)

    def convert_abbreviation(chosung_char, jungsung_char, jongsung_char, hangul_abbreviations_syllable, hangul_initials, hangul_medials, hangul_finals):
        combined = ""

        # 초성이 ㅇ인 경우
        if chosung_char == 'ㅇ':
            # 종성이 있는 경우
            if jongsung_char:
                # 초성+중성+종성이 약자에 해당하는 경우
                if 'ㅇ' + jungsung_char + jongsung_char in hangul_abbreviations_syllable:
                    combined = hangul_abbreviations_syllable['ㅇ' + jungsung_char + jongsung_char]
                else:
                    # 약자 변환에 실패한 경우, 개별 변환
                    combined = chosung_char + jungsung_char + jongsung_char
            else:
                # 종성이 없는 경우, 중성 값만 변환
                combined = jungsung_char
        # 초성이 ㅇ이 아닌 경우
        else:
            # ㅇ+중성+종성이 약자에 해당하는 경우
            if 'ㅇ' + jungsung_char + jongsung_char in hangul_abbreviations_syllable:
                combined = chosung_char + hangul_abbreviations_syllable['ㅇ' + jungsung_char + jongsung_char]
            # 초성+중성+종성이 약자에 해당하는 경우
            elif chosung_char + jungsung_char + jongsung_char in hangul_abbreviations_syllable:
                combined = hangul_abbreviations_syllable[chosung_char + jungsung_char + jongsung_char]
            # 초성+중성이 약자에 해당하는 경우
            elif chosung_char + jungsung_char in hangul_abbreviations_syllable:
                # 종성이 있는 경우
                if jongsung_char:
                    combined = hangul_abbreviations_syllable[chosung_char + jungsung_char] + jongsung_char
                else:
                    combined = hangul_abbreviations_syllable[chosung_char + jungsung_char]
            else:
                # 약자 변환에 실패한 경우, 개별 변환
                combined = chosung_char + jungsung_char + jongsung_char
    
        return combined
    
    def convert_char_to_braille(char):
        # 영어 대문자를 소문자로 변환 및 대문자 처리
        if 'A' <= char <= 'Z':
            return '03' + braille_dict.get(char.lower(), '')
        # 한글 처리
        if ord('가') <= ord(char) <= ord('힣'):
            base_code = ord(char) - ord('가')
            chosung_index = base_code // 588
            jungsung_index = (base_code - (chosung_index * 588)) // 28
            jongsung_index = base_code % 28
    
            chosung_char = chr(chosung_index + ord('ㄱ'))
            jungsung_char = chr(jungsung_index + ord('ㅏ'))
            jongsung_char = chr(jongsung_index + ord('ㄱ') - 1) if jongsung_index > 0 else ''
    
            # 초성이 'ㅇ'인 경우, 변환에서 제외
            #if chosung_char == 'ㅇ':
                #chosung_char = ''
            #else:
            chosung_char = hangul_initials.get(chosung_char, '')
            jungsung_char = hangul_medials.get(jungsung_char, '')
            jongsung_char = hangul_finals.get(jongsung_char, '')
            
            # 초성, 중성, 종성을 약자 변환 함수로 변환
            return convert_abbreviation(chosung_char, jungsung_char, jongsung_char, hangul_abbreviations_syllable, hangul_initials, hangul_medials, hangul_finals)
        else:
            # 영문 소문자, 숫자 및 기호 처리
            return braille_dict.get(char, '')


    braille_texts = []
    for text in text_list:
        braille_text = ''
        # 약자 처리
        if text in hangul_abbreviations_word:
            braille_text += hangul_abbreviations_word[text]
        else:    
            # 영어 문자로만 구성된 경우
            if is_english(text):
                braille_text = '36' + ''.join([convert_char_to_braille(char) for char in text])
            # 숫자로만 구성된 경우
            elif text.isdigit():
                braille_text = '37' + ''.join([convert_char_to_braille(char) for char in text])
            else:
                for char in text:
                    if char in hangul_abbreviations_syllable:
                        braille_text += hangul_abbreviations_syllable[char]
                    else:
                        braille_text += convert_char_to_braille(char)
        braille_texts.append(braille_text)
    
    return braille_texts


# 테스트 코드
test_texts = [
    "Hello",
    "안녕하세요",
    "38",
    "가나다라마바사",
    "그런데",
    "간"
]

braille_results = text_to_braille(test_texts)

for original, braille in zip(test_texts, braille_results):
    print(f"Original: {original}")
    print(f"Braille: {braille}")
    print()


# In[19]:


def convert_abbreviation(text):
    hangul_initials = {
        'ㄱ': '01', 'ㄴ': '11', 'ㄷ': '21', 'ㄹ': '02', 'ㅁ': '12', 'ㅂ': '04',
        'ㅅ': '03', 'ㅇ': '66', 'ㅈ': '50', 'ㅊ': '60', 'ㅋ': '62', 'ㅌ': '63',
        'ㅍ': '26', 'ㅎ': '36'
    }
    
    hangul_medials = {
        'ㅏ': '43', 'ㅑ': '34', 'ㅓ': '61', 'ㅕ': '16', 'ㅗ': '53', 'ㅛ': '35',
        'ㅜ': '51', 'ㅠ': '15', 'ㅡ': '25', 'ㅣ': '52', 'ㅢ': '27', 'ㅔ': '54',
        'ㅐ': '72', 'ㅖ': '31', 'ㅘ': '73', 'ㅝ': '71', 'ㅚ': '57', 'ㅟ': '5172', 
        'ㅒ': '3472', 'ㅙ': '7372', 'ㅞ': '7172'
    }
    
    hangul_finals = {
        'ㄱ': '10', 'ㄴ': '22', 'ㄷ': '32', 'ㄹ': '20', 'ㅁ': '23', 'ㅂ': '40',
        'ㅅ': '30', 'ㅇ': '66', 'ㅈ': '50', 'ㅊ': '60', 'ㅋ': '62', 'ㅌ': '63',
        'ㅍ': '26', 'ㅎ': '36'
    }
    
    hangul_abbreviations_syllable = {
        '가': '45', '나': '11', '다': '21', '마': '12', '바': '04', '사': '70', 
        '자': '05', '카': '41', '타': '42', '파': '14', '하': '24', '억': '17', 
        '언': '67', '얼': '64', '연': '13', '열': '46', '영': '47', '옥': '55',
        '온': '76', '옹': '77', '운': '44', '울': '75', '은': '56', '을': '65', 
        '인': '74', '것': '0761'
    }
    
    hangul_abbreviations_word = {
        '그러나': '1011', '그러면': '1022', '그래서': '1061', '그런데': '1054',
        '그러므로': '1023', '그리고': '1053', '그리하여': '1016'
    }
    
    # 변환 결과를 저장할 변수
    result = ""
    
    # 먼저 단어 약자를 처리
    for word, code in hangul_abbreviations_word.items():
        if word in text:
            text = text.replace(word, code)
    
    # 다음으로 음절 약자를 처리
    for syllable, code in hangul_abbreviations_syllable.items():
        if syllable in text:
            text = text.replace(syllable, code)
    
    # 나머지 글자들을 처리
    for char in text:
        if ord('가') <= ord(char) <= ord('힣'):
            # 초성, 중성, 종성 분리
            initial_index = (ord(char) - ord('가')) // 588
            medial_index = ((ord(char) - ord('가')) % 588) // 28
            final_index = (ord(char) - ord('가')) % 28
            
            # 초성 값 추가
            initial = chr(0x1100 + initial_index)
            if initial in hangul_initials:
                result += hangul_initials[initial]
            
            # 중성 값 추가
            medial = chr(0x1161 + medial_index)
            if medial in hangul_medials:
                result += hangul_medials[medial]
            
            # 종성 값 추가 (종성이 없을 경우 처리하지 않음)
            if final_index != 0:
                final = chr(0x11A7 + final_index)
                if final in hangul_finals:
                    result += hangul_finals[final]
        else:
            result += char
    
    return result

# 테스트
print(convert_abbreviation('간'))          # 기대 출력: 4522
print(convert_abbreviation('안녕하세요'))  # 기대 출력: 4322114614032753
print(convert_abbreviation('가나다라마바사')) # 기대 출력: 4511210243120470


# In[ ]:




