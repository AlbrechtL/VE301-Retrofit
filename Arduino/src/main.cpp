#include <Arduino.h>
#include <CapacitorLite.h>
#include <simpleRPC.h>

CapacitorLite cap0(6,A0);
CapacitorLite cap1(5,A1);

void setup() {
  Serial.begin(115200);
}

unsigned int getCap0(void) {
  return cap0.Measure();
}
unsigned int getCap1(void) {
  return cap1.Measure();
}

void loop() {
  interface(
    Serial,
    getCap0, F("getCap0: Reads the capacitor value between dataPin 6 and analog pin A0. @return: Capacitor value."),
    getCap1, F("getCap1: Reads the capacitor value between dataPin 5 and analog pin A1. @return: Capacitor value."));
  // Serial.print("cap0: ");
  // Serial.print(getCap0());
  // Serial.print("     cap1: ");
  // Serial.println(getCap1());
  // delay(100);
}
