#include <Servo.h>

// 버튼 핀 설정
int buttonPin1 = 11;
int buttonPin2 = 12;
int buttonPin3 = 13;

// 서보 모터 객체 배열
Servo servos[18];

// 서보 모터 핀 번호 배열
int servoPins[18] = {22, 23, 26, 27, 30, 31, 34, 35, 38, 39, 42, 43, 46, 47, 50, 51, 52, 53};

// 서버로부터 받은 문자열 저장
String receivedStr = ""; // 서버로부터 받은 문자열

// 서버로부터 받은 문자열 목록
String receivedStrList[18]; // 최대 18개의 문자열 저장
int currentIndex = -1; // 현재 인덱스 초기화

// 서버로부터 받은 문자에 따른 각도 설정
int angles[18]; // 문자에 따른 각도를 저장할 배열

void setup() {
  Serial.begin(9600);
  
  // 버튼 핀 설정
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  
  // 서보 모터 핀 설정
  for (int i = 0; i < 18; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(0);
  }
}

void loop() {
  if (Serial.available() > 0) {
    // 도착한 데이터를 읽어 receivedStr에 저장
    String tempStr = Serial.readStringUntil('\n');
    tempStr.trim(); // 문자열의 앞뒤 공백 제거
    
    // 받은 데이터가 명령어가 아닐 경우에만 receivedStr에 저장
    if (tempStr != "Take Picture" && tempStr != "Previous" && tempStr != "Next") {
      receivedStr = tempStr;
      currentIndex++;
      receivedStrList[currentIndex % 18] = receivedStr; // 받은 문자열을 리스트에 저장
      setAngles(receivedStr); // 바로 서보 모터 각도 설정
    }
  }
  
  if (digitalRead(buttonPin1) == LOW) {
    Serial.println("Take Picture");
    delay(1000); // 디바운싱 딜레이
  }
  else if (digitalRead(buttonPin2) == LOW) {
    Serial.println("Previous");
    if (currentIndex > 0) {
      currentIndex--;
      receivedStr = receivedStrList[currentIndex % 18];
      setAngles(receivedStr); // 이전 문자열에 따른 각도 설정
    }
    delay(1000); // 디바운싱 딜레이
  }
  else if (digitalRead(buttonPin3) == LOW) {
    Serial.println("Next");
    if (currentIndex < 17 && receivedStrList[(currentIndex + 1) % 18].length() != 0) {
      currentIndex++;
      receivedStr = receivedStrList[currentIndex % 18];
      setAngles(receivedStr); // 다음 문자열에 따른 각도 설정
    }
    delay(1000); // 디바운싱 딜레이
  }
}

// 문자열에 따른 서보 모터 각도 설정 함수
void setAngles(String str) {
  for (int i = 0; i < 18; i++) {
    if (i < str.length()) {
      // 문자열에서 각 문자를 숫자로 변환하고 해당하는 각도로 설정
      int index = str.charAt(i) - '0'; // 문자를 숫자로 변환
      angles[i] = index * 25; // 0~7까지 각 숫자에 맞는 각도 설정
    } else {
      // 나머지 서보 모터의 각도를 0으로 설정
      angles[i] = 0;
    }
    servos[i].write(angles[i]); // 각도 설정
  }
}