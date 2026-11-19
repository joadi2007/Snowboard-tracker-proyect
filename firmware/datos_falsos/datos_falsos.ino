const int FS = 100;                          // muestras por segundo
const unsigned long PERIODO_MS = 1000 / FS;  // 10 ms entre muestras

unsigned long ultimo = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("t,ax,ay,az,gx,gy,gz");
}

void loop() {
  unsigned long ahora = millis();

  if (ahora - ultimo >= PERIODO_MS) {
    ultimo = ahora;

    float t  = ahora / 1000.0;
    float ax = random(-30, 31) / 100.0;
    float ay = random(-30, 31) / 100.0;
    float az = 9.81 + random(-30, 31) / 100.0;
    float gx = random(-20, 21) / 10.0;
    float gy = random(-20, 21) / 10.0;
    float gz = random(-20, 21) / 10.0;

    Serial.print(t, 3);  Serial.print(",");
    Serial.print(ax, 2); Serial.print(",");
    Serial.print(ay, 2); Serial.print(",");
    Serial.print(az, 2); Serial.print(",");
    Serial.print(gx, 2); Serial.print(",");
    Serial.print(gy, 2); Serial.print(",");
    Serial.println(gz, 2);
  }
}