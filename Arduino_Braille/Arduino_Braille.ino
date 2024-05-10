int buttonPin1 = 2;  // 버튼 1 연결 핀
int buttonPin2 = 3;  // 버튼 2 연결 핀
int buttonPin3 = 4;  // 버튼 3 연결 핀

void setup() {
  Serial.begin(9600); // 시리얼 통신 속도 설정
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
}

void loop() {
  if (digitalRead(buttonPin1) == HIGH) {
    Serial.println("Take Picture");
    delay(1000); // 디바운싱을 위한 딜레이
  }
  else if (digitalRead(buttonPin2) == HIGH) {
    Serial.println("Next");
    delay(1000); // 디바운싱을 위한 딜레이
  }
  else if (digitalRead(buttonPin3) == HIGH) {
    Serial.println("Previous");
    delay(1000); // 디바운싱을 위한 딜레이
  }
}