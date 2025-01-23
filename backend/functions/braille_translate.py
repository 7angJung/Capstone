#!/usr/bin/env python
# coding: utf-8

# In[111]:


get_ipython().system('pip install jamo')


# In[2]:


from unicode import join_jamos
from jamo import h2j, j2hcj

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
        '‘': '0363', '’': '3630', '-': '33', '(': '6330', ')': '0336',
        '/': '0731', "\\": '360127', '@':'0110'
    }
    hangul_initials = {
        # 한글 점자 초성 
        'ㄱ': '01', 'ㄴ': '11', 'ㄷ': '21', 'ㄹ': '02', 'ㅁ': '12', 'ㅂ': '04',
        'ㅅ': '03', 'ㅇ': '66', 'ㅈ': '05', 'ㅊ': '06', 'ㅋ': '41', 'ㅌ': '42',
        'ㅍ': '14', 'ㅎ': '24', 'ㄲ':'0301', 'ㄸ':'0321', 'ㅃ':'0304', 'ㅆ':'0303',
        'ㅉ':'0305'
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
        'ㅍ': '26', 'ㅎ': '36', 'ㄳ': '1030', 'ㄵ': '2250', 'ㄶ': '2236', 'ㄺ': '2010',
        'ㄻ': '2023', 'ㄼ': '2040', 'ㄽ':'2030', 'ㄾ':'2063', 'ㄿ':'2026', 'ㅀ':'2036',  
        'ㅄ': '2330', 'ㅆ': '31'
    }

    plain_initials = {
        'ㄲ': 'ㄱ',
        'ㄸ': 'ㄷ',
        'ㅃ': 'ㅂ',
        'ㅆ': 'ㅅ',
        'ㅉ': 'ㅈ'
    }
    
    hangul_abbreviations_syllable = {
        # 한글 점자 음절 약자 
        '가': '45', '나': '11', '다': '21', '마': '12', '바': '04', '사': '70', 
        '자': '05', '카': '41', '타': '42', '파': '14', '하': '24', '억': '17', 
        '언': '67', '얼': '64', '연': '13', '열': '46', '영': '47', '옥': '55',
        '온': '76', '옹': '77', '운': '44', '울': '75', '은': '56', '을': '65', 
        '인': '74', '것': '0761', '성': '0347', '정': '5047', '청': '6047'
    }
    hangul_abbreviations_word = {
        # 한글 점자 단어 약자 
        '그러나': '1011', '그러면': '1022', '그래서': '1061', '그런데': '1054',
        '그러므로': '1023', '그리고': '1053', '그리하여': '1016'
    }
    
    # 텍스트가 영어인지 확인
    def is_english(text):
        return all('A' <= char <= 'Z' or 'a' <= char <= 'z' for char in text)

    # 텍스트가 한글인지 확인인
    def is_hangul(text):
        for char in text:
            # 완성형 한글 검사
            if '\uAC00' <= char <= '\uD7A3':
                continue
            # 한글 자모 검사
            elif '\u1100' <= char <= '\u11FF' or '\uA960' <= char <= '\uA97F' or '\uD7B0' <= char <= '\uD7FF' or '\u3130' <= char <= '\u318F':
                continue
            else:
                return False
        return True

    
    # 약자 변환
    def convert_abbreviation(chosung_char, jungsung_char, jongsung_char):
        combined = ''

        if chosung_char == 'ㅇ':
            if not jongsung_char:
                # 초성 'ㅇ', 종성 없음
                combined = hangul_medials.get(jungsung_char, '')
            else:
                abbr_key = join_jamos(chosung_char + jungsung_char + jongsung_char)
                if abbr_key in hangul_abbreviations_syllable:
                    # 초성 'ㅇ', 중성+종성이 약자에 해당
                    combined = hangul_abbreviations_syllable.get(abbr_key, '')
                else:
                    # 초성 'ㅇ', 중성+종성이 약자에 해당하지 않음
                    combined = hangul_medials.get(jungsung_char, '') + hangul_finals.get(jongsung_char, '')
        else:
            if not jongsung_char:
                abbr_key = join_jamos(chosung_char + jungsung_char)
                if abbr_key in hangul_abbreviations_syllable:
                    # 초성+중성이 약자에 해당
                    combined = hangul_abbreviations_syllable.get(abbr_key, '')
                else:
                    # 초성+중성이 약자에 해당하지 않음
                    combined = hangul_initials.get(chosung_char, '') + hangul_medials.get(jungsung_char, '')
            else:
                abbr_key_full = join_jamos(chosung_char + jungsung_char + jongsung_char)
                abbr_key_partial = join_jamos(chosung_char + jungsung_char)
                abbr_key_initial_jungjong = join_jamos('ㅇ' + jungsung_char + jongsung_char)

                if abbr_key_full in hangul_abbreviations_syllable:
                    combined = hangul_abbreviations_syllable.get(abbr_key_full, '')
                elif abbr_key_partial in hangul_abbreviations_syllable:
                    # 초성+중성이 약자에 해당
                    combined = hangul_abbreviations_syllable.get(abbr_key_partial, '') + hangul_finals.get(jongsung_char, '')
                elif abbr_key_initial_jungjong in hangul_abbreviations_syllable:
                    # 'ㅇ'+중성+종성이 약자에 해당
                    combined = hangul_initials.get(chosung_char, '') + hangul_abbreviations_syllable[abbr_key_initial_jungjong]
                else:
                    # 초성, 중성, 종성을 각각 점자로 변환
                    combined = hangul_initials.get(chosung_char, '') + hangul_medials.get(jungsung_char, '') + hangul_finals.get(jongsung_char, '')
    
        return combined


    # 텍스트 점자로 변환
    def convert_char_to_braille(char):
        if 'A' <= char <= 'Z':
            return '03' + braille_dict.get(char.lower(), '')

        return braille_dict.get(char, '')

    print("텍스트를 점자로 변환 중입니다...")
    
    braille_texts = []
    for text in text_list:
        braille_text = ''
        if text in hangul_abbreviations_word:
            braille_text = hangul_abbreviations_word.get(text, '')
        else:
            if is_english(text):
                braille_text = '36' + ''.join([convert_char_to_braille(char) for char in text]) + '26'
            elif text.isdigit():
                braille_text = '37' + ''.join([convert_char_to_braille(char) for char in text])
            elif is_hangul(text):
                for char in text:
                    if char in hangul_abbreviations_syllable:
                        braille_text += hangul_abbreviations_syllable.get(char, '')
                        continue
                    else:
                        jamo_chars = j2hcj(h2j(char))
                        # 분리된 자모를 각각의 변수에 저장
                        chosung_char = jamo_chars[0]  # 초성
                        jungsung_char = jamo_chars[1]  # 중성
                        jongsung_char = jamo_chars[2] if len(jamo_chars) > 2 else ''  # 종성 (없을 수도 있음)
                        braille_text += convert_abbreviation(chosung_char, jungsung_char, jongsung_char)
            else:
                for char in text:
                    if is_hangul(char):
                        if char in hangul_abbreviations_syllable:
                            braille_text += hangul_abbreviations_syllable.get(char, '')
                            continue
                        else:
                            jamo_chars = j2hcj(h2j(char))
                            # 분리된 자모를 각각의 변수에 저장
                            chosung_char = jamo_chars[0]  # 초성
                            jungsung_char = jamo_chars[1]  # 중성
                            jongsung_char = jamo_chars[2] if len(jamo_chars) > 2 else ''  # 종성 (없을 수도 있음)
                            braille_text += convert_abbreviation(chosung_char, jungsung_char, jongsung_char)
                            braille_text += hangul_abbreviations_syllable.get(char, '')
                            continue
                    elif is_english(char):
                        braille_text += '36' + convert_char_to_braille(char) + '26'
                    elif char.isdigit():
                        braille_text += '37' + convert_char_to_braille(char)
                    else:
                        braille_text += convert_char_to_braille(char)
                
        braille_texts.append(braille_text)

    print("점자 변환이 완료됐습니다.")
    return braille_texts

