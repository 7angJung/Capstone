#include <Servo.h>

// 버튼 핀 설정
int buttonPin1 = 11; // 사진 촬영 버튼
int buttonPin2 = 12; // 이전 각도 설정 버튼
int buttonPin3 = 13; // 다음 각도 설정 버튼

// 서보 모터 객체 배열
Servo servos[18];

// 서보 모터 핀 번호 배열
int servoPins[18] = {22, 23, 26, 27, 30, 31, 34, 35, 38, 39, 42, 43, 46, 47, 50, 51, 52, 53};

// 서버로부터 받은 문자열 저장
String receivedStr = ""; // 서버로부터 받은 문자열

// 서버로부터 받은 문자열 목록
String receivedStrList[18]; // 최대 18개의 문자열 저장
int currentIndex = -1; // 현재 인덱스 초기화

// 서버로부터 받은 문자에 따른 시간 설정
double times[18] = {0}; // 문자에 따른 시간을 저장할 배열
double previousTimes[18] = {0}; // 이전 시간을 저장할 배열, 초기값을 모두 0으로 설정

void setup() {
  Serial.begin(9600);
  
  // 버튼 핀 설정
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  
  // 서보 모터 핀 설정 및 초기화
  for (int i = 0; i < 18; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90); // 모든 서보 모터를 정지 상태로 초기화
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
      setTime(receivedStr); // 시간 설정
    }
  }
  
  if (digitalRead(buttonPin1) == LOW) {
    Serial.println("Take Picture");
    resetTimes(); // times와 previousTimes 배열 초기화
    delay(1000); // 디바운싱 딜레이
  }
  else if (digitalRead(buttonPin2) == LOW) {
    Serial.println("Previous");
    if (currentIndex > 0) {
      currentIndex--;
      receivedStr = receivedStrList[currentIndex % 18];
      initializeServos(); // 서보 모터 초기화
      rotateServos(receivedStr); // 이전 문자열에 따른 서보 모터 회전
    }
    delay(1000); // 디바운싱 딜레이
  }
  else if (digitalRead(buttonPin3) == LOW) {
    Serial.println("Next");
    if (currentIndex < 17 && receivedStrList[(currentIndex + 1) % 18].length() != 0) {
      currentIndex++;
      receivedStr = receivedStrList[currentIndex % 18];
      initializeServos(); // 서보 모터 초기화
      rotateServos(receivedStr); // 다음 문자열에 따른 서보 모터 회전
    }
    delay(1000); // 디바운싱 딜레이
  }
}

// 문자열에 따른 서보 모터 시간 설정 함수
void setTime(String str) {
  for (int i = 0; i < 18; i++) {
    if (i < str.length()) {
      // 문자열에서 각 문자를 숫자로 변환하고 해당하는 시간 설정
      int index = str.charAt(i) - '0'; // 문자를 숫자로 변환
      previousTimes[i] = times[i]; // 이전 시간 저장
      times[i] = index * 400; // 각 숫자에 맞는 실행 시간을 설정 (0~7)
    } else {
      // 나머지 서보 모터의 시간을 0으로 설정
      previousTimes[i] = times[i]; // 이전 시간 저장
      times[i] = 0;
    }
  }
}

// 서보 모터 회전 함수
void rotateServos(String str) {
  for (int i = 0; i < 18; i++) {
    if (i < str.length()) {
      // 정방향으로 회전
      servos[i].write(70); // 정방향 느린속도
      delay(times[i]); // 지정된 시간만큼 대기
      servos[i].write(90); // 정지
    }
  }
}

// 서보 모터 초기화 함수
void initializeServos() {
  for (int i = 0; i < 18; i++) {
    // 역방향으로 회전
    servos[i].write(100); // 역방향 느린속도
    delay(previousTimes[i]); // 이전에 설정된 시간만큼 대기
    servos[i].write(90); // 정지
  }
}

// times와 previousTimes 배열 초기화 함수
void resetTimes() {
  for (int i = 0; i < 18; i++) {
    times[i] = 0; // 모든 값 0으로 초기화
    previousTimes[i] = 0; // 모든 값 0으로 초기화
  }
}