#include "braille.h"

// Define the pins for the braille module
int dataPin = 5;   // DATA pin number
int latchPin = 6;  // LATCH pin number
int clockPin = 7;  // CLOCK pin number
int no_module = 3; // Number of braille output modules

// Create an instance of the braille class
braille bra(dataPin, latchPin, clockPin, no_module);

char string_buffer[100];                // Received string
char string_buffer_serial[100][4];       // Split string buffer
int str_char_count = 0;                  // Total number of characters

int buttonPin1 = 2;  // 버튼 1 연결 핀
int buttonPin2 = 3;  // 버튼 2 연결 핀
int buttonPin3 = 4;  // 버튼 3 연결 핀

byte hangul_cho[19] = {
  0b00010000,//ㄱ
  0b00010000,//ㄲ
  0b00110000,//ㄴ
  0b00011000,//ㄷ
  0b00011000,//ㄸ
  0b00000100,//ㄹ
  0b00100100,//ㅁ
  0b00010100,//ㅂ
  0b00010100,//ㅃ
  0b00000001,//ㅅ
  0b00000001,//ㅆ
  0b00111100,//o
  0b00010001,//ㅈ
  0b00010001,//ㅉ
  0b00000101,//ㅊ
  0b00111000,//ㅋ
  0b00101100,//ㅌ
  0b00110100,//ㅍ
  0b00011100 //ㅎ
};

byte hangul2_cho[19] = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
};

byte hangul_jung[21] = {
  0b00101001, // ㅏ
  0b00101110, // ㅐ
  0b00010110, // ㅑ
  0b00010110, // ㅒ
  0b00011010, // ㅓ
  0b00110110, // ㅔ
  0b00100101, // ㅕ
  0b00010010, // ㅖ
  0b00100011, // ㅗ
  0b00101011, // ㅘ
  0b00101011, // ㅙ
  0b00110111, // ㅚ
  0b00010011, // ㅛ
  0b00110010, // ㅜ
  0b00111010, // ㅝ
  0b00111010, // ㅞ
  0b00110010, // ㅟ
  0b00110001, // ㅠ
  0b00011001, // ㅡ
  0b00011101, // ㅢ
  0b00100110 // ㅣ
};

byte hangul2_jung[21] = {
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
};

byte hangul_jong[28] = {
  0b00000000, // 없음
  0b00100000, // ㄱ
  0b00100000, // ㄲ
  0b00100000, // ㄳ
  0b00001100, // ㄴ
  0b00001100, // ㄵ
  0b00001100, // ㄶ
  0b00000110, // ㄷ
  0b00001000, // ㄹ
  0b00001000, // ㄺ
  0b00001000, // ㄻ
  0b00001000, // ㄼ
  0b00001000, // ㄽ
  0b00001000, // ㄾ
  0b00001000, // ㄿ
  0b00001000, // ㅀ
  0b00001001, // ㅁ
  0b00101000, // ㅂ
  0b00101000, // ㅄ
  0b00000010, // ㅅ
  0b00000010, // ㅆ
  0b00001111, // ㅇ
  0b00100010, // ㅈ
  0b00001010, // ㅊ
  0b00001110, // ㅋ
  0b00001011, // ㅌ
  0b00001101, // ㅍ
  0b00000111 // ㅎ
};

byte hangul2_jong[28] = {
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
};

byte ascii_data[127] = {
  0b00000000, // 0
  0b00000000, // 1
  0b00000000, // 2
  0b00000000, // 3
  0b00000000, // 4
  0b00000000, // 5
  0b00000000, // 6
  0b00000000, // 7
  0b00000000, // 8
  0b00000000, // 9
  0b00000000, // 10
  0b00000000, // 11
  0b00000000, // 12
  0b00000000, // 13
  0b00000000, // 14
  0b00000000, // 15
  0b00000000, // 16
  0b00000000, // 17
  0b00000000, // 18
  0b00000000, // 19
  0b00000000, // 20
  0b00000000, // 21
  0b00000000, // 22
  0b00000000, // 23
  0b00000000, // 24
  0b00000000, // 25
  0b00000000, // 26
  0b00000000, // 27
  0b00000000, // 28
  0b00000000, // 29
  0b00000000, // 30
  0b00000000, // 31
  0b00000000, // 32 SPACE
  0b00001110, // 33 !
  0b00001011, // 34 "
  0b00000000, // 35 #
  0b00000000, // 36 $
  0b00010010, // 37 %
  0b00000000, // 38 &
  0b00000000, // 39 '
  0b00001011, // 40 (
  0b00000001, // 41 )
  0b00100001, // 42 *
  0b00001001, // 43 +
  0b00000100, // 44 ,
  0b00000110, // 45 -
  0b00001101, // 46 .
  0b00010101, // 47 /
  0b00011100, // 48 0
  0b00100000, // 49 1
  0b00101000, // 50 2
  0b00110000, // 51 3
  0b00110100, // 52 4
  0b00100100, // 53 5
  0b00111000, // 54 6
  0b00111100, // 55 7
  0b00101100, // 56 8
  0b00011000, // 57 9
  0b00000100, // 58 :
  0b00000101, // 59 ;
  0b00000100, // 60 <
  0b00001100, // 61 =
  0b00000111, // 62 >
  0b00001011, // 63 ?
  0b00000000, // 64 @
  0b00100000, // 65 A
  0b00101000, // 66 B
  0b00110000, // 67 C
  0b00110100, // 68 D
  0b00100100, // 69 E
  0b00111000, // 70 F
  0b00111100, // 71 G
  0b00101100, // 72 H
  0b00011000, // 73 I
  0b00011100, // 74 J
  0b00100010, // 75 K
  0b00101010, // 76 L
  0b00110010, // 77 M
  0b00110110, // 78 N
  0b00100110, // 79 O
  0b00111010, // 80 P
  0b00111110, // 81 Q
  0b00101110, // 82 R
  0b00011010, // 83 S
  0b00011110, // 84 T
  0b00100011, // 85 U
  0b00101011, // 86 V
  0b00011101, // 87 W
  0b00110011, // 88 X
  0b00110111, // 89 Y
  0b00100111, // 90 Z
  0b00001011, // 91 [
  0b00010000, // 92 \
  0b00000101, // 93 ]
  0b00000000, // 94 ^
  0b00000011, // 95 _
  0b00000000, // 96 '
  0b00100000, // 97 a
  0b00101000, // 98 b
  0b00110000, // 99 c
  0b00110100, // 100 d
  0b00100100, // 101 e
  0b00111000, // 102 f
  0b00111100, // 103 g
  0b00101100, // 104 h
  0b00011000, // 105 i
  0b00011100, // 106 j
  0b00100010, // 107 k
  0b00101010, // 108 l
  0b00110010, // 109 m
  0b00110110, // 110 n
  0b00100110, // 111 o
  0b00111010, // 112 p
  0b00111110, // 113 q
  0b00101110, // 114 r
  0b00011010, // 115 s
  0b00011110, // 116 t
  0b00100011, // 117 u
  0b00101011, // 118 v
  0b00011101, // 119 w
  0b00110011, // 120 x
  0b00110111, // 121 y
  0b00100111, // 122 z
  0b00001011, // 123 {
  0b00000000, // 124 |
  0b00000100, // 125 }
  0b00000000, // 126 ~
};

String incomingText = ""; // 수신된 문자열을 저장할 변수

void setup() {
  Serial.begin(9600);
  bra.begin();
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  delay(1000);
  bra.all_off();
  bra.refresh();
}

void loop() {
  if (digitalRead(buttonPin1) == LOW) {
    Serial.println("Take Picture");
    delay(1000); // 디바운싱을 위한 딜레이
  }
  else if (digitalRead(buttonPin2) == LOW) {
    Serial.println("Next");
    delay(1000); // 디바운싱을 위한 딜레이
  }
  else if (digitalRead(buttonPin3) == LOW) {
    Serial.println("Previous");
    delay(1000); // 디바운싱을 위한 딜레이
  }
  
  if (Serial.available()) {
    char receivedChar = Serial.read();

    if (receivedChar == '\n') {
      for (unsigned int i = 0; i < incomingText.length(); i++) {
        display(incomingText[i]);
        delay(1000); // 다음 문자로 넘어가기 전에 지연
      }
      incomingText = ""; // 문자열 초기화
    } else {
      incomingText += receivedChar; // 수신된 문자 추가
    }
  }
}

void display(uint8_t ch) {
  int index = 0;
  if (ch >= 'a' && ch <= 'z') {
    index = ch - 'a';
  } else if (ch >= 'A' && ch <= 'Z') {
    index = ch - 'A';
  } else {
    off();
    return;
  }

  for (int i = 0; i < 6; i++) {
    int value = (ascii_data[index] >> (5 - i)) & 0b00000001;
    if (value) {
      bra.on(0, i);
    } else {
      bra.off(0, i);
    }
  }
  bra.refresh();
}

void off() {
  for (int i = 0; i < 6; i++) {
    bra.off(0, i);
  }
  bra.refresh();
}