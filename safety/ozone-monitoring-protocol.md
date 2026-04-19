# Ozone Monitoring Protocol

**Applicable to:** All atmospheric-pressure DBD prototypes (2, 4, 5, 6, 7)
**Not required for:** Sealed argon systems at <10 Torr (Prototype 3)

## Hardware

- **Sensor:** MQ-131 ozone sensor module
- **Controller:** Arduino Nano (shared with PWM controller)
- **Calibration:** Factory-calibrated; verify against known ozone source annually

## Thresholds

| Level | Concentration | Action |
|-------|--------------|--------|
| Normal | <10 ppb | Continue operation |
| Warning | 10–14 ppb | Audible alarm, increase ventilation |
| Shutdown | ≥15 ppb | Auto-shutoff of ZVS driver |
| Regulatory limit | 20 ppb (8-hr avg) | Health Canada RIAQG maximum |

## Arduino Integration

```cpp
// MQ-131 Ozone Monitor — Arduino Nano
// Connects to Bayesian controller via Serial

#define MQ131_PIN A0
#define ALARM_PIN 8
#define RELAY_PIN 9  // ZVS power relay

const float WARNING_PPB = 10.0;
const float SHUTDOWN_PPB = 15.0;

void setup() {
  Serial.begin(115200);
  pinMode(ALARM_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);  // ZVS on
}

void loop() {
  float raw = analogRead(MQ131_PIN);
  float ppb = convertToPPB(raw);  // Calibration function
  
  Serial.print("OZONE:");
  Serial.println(ppb, 1);
  
  if (ppb >= SHUTDOWN_PPB) {
    digitalWrite(RELAY_PIN, LOW);   // ZVS off
    digitalWrite(ALARM_PIN, HIGH);  // Alarm on
    Serial.println("STATUS:SHUTDOWN");
  } else if (ppb >= WARNING_PPB) {
    digitalWrite(ALARM_PIN, HIGH);
    Serial.println("STATUS:WARNING");
  } else {
    digitalWrite(ALARM_PIN, LOW);
    Serial.println("STATUS:NORMAL");
  }
  
  delay(1000);  // 1 Hz sampling
}

float convertToPPB(float raw) {
  // MQ-131 calibration curve (sensor-specific)
  // Adjust coefficients based on datasheet and calibration
  float voltage = raw * (5.0 / 1023.0);
  float rs = (5.0 - voltage) / voltage * 10.0;  // Load resistor 10k
  float ratio = rs / 30.0;  // R0 calibration value
  return 100.0 * pow(ratio, -1.67);  // Approximate curve
}
```

## Logging

All ozone readings are logged to SD card (if present) and transmitted via Serial to the Bayesian controller for real-time integration into the digital twin safety overlay.
