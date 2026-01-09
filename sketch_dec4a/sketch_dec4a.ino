void setup() {
  Serial.begin(115200);
  pinMode(4, INPUT);
}

void loop() {
  unsigned long t = pulseIn(4, HIGH, 50000);
  Serial.println(t);
}
