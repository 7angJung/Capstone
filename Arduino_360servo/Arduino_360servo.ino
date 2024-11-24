#include <Servo.h>

// 서보 모터 객체 배열
Servo servos[18];

// 서보 모터 핀 번호 배열
int servoPins[18] = {22, 23, 26, 27, 30, 31, 34, 35, 38, 39, 42, 43, 46, 47, 50, 51, 52, 53};

void setup() {
  Serial.begin(9600);
  
  // 서보 모터 핀 설정
  for (int i = 0; i < 18; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(0); // 초기 각도 0도로 설정
  }
}

void loop() {
  for (int i = 0; i < 18; i++) {
    // 서보 모터를 0도에서 175도까지 회전
    servos[i].write(157.5);
    delay(1000); // 1초 대기
    // 서보 모터를 다시 0도로 회전
    servos[i].write(0);
    delay(1000); // 1초 대기
    // 다음 서보 모터를 위해 0.5초 대기
    delay(500);
  }

  // 모든 행동을 멈추고 0도에서 대기
  while (true) {
    // 무한 루프
  }
}

