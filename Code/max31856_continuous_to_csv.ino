#include <Adafruit_MAX31856.h>

#define DRDY_PIN 5

Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(10);

unsigned long startTime;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  pinMode(DRDY_PIN, INPUT);

  if (!maxthermo.begin()) {
    Serial.println("Could not initialize thermocouple.");
    while (1) delay(10);
  }

  maxthermo.setThermocoupleType(MAX31856_TCTYPE_T);
  maxthermo.setConversionMode(MAX31856_CONTINUOUS);

  // Print CSV header
  Serial.println("time_s,temp_c,cold_junction_c");

  startTime = millis();
}

void loop() {
  while (digitalRead(DRDY_PIN)) {}  // wait for conversion ready

  float elapsed = (millis() - startTime) / 1000.0;
  float temp = maxthermo.readThermocoupleTemperature();
  float cold = maxthermo.readCJTemperature();

  Serial.print(elapsed, 2);
  Serial.print(",");
  Serial.print(temp, 2);
  Serial.print(",");
  Serial.println(cold, 2);

  //delay(500);
}