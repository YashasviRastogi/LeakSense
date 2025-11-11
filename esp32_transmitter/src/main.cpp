#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>

// LoRa Pin Configuration for ESP32
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

// LoRa Frequency (433 MHz, 868 MHz, or 915 MHz)
#define LORA_FREQUENCY 915E6

// Sensor Pin Configuration
#define PRESSURE_SENSOR_PIN 34    // Analog pin for pressure sensor
#define MOISTURE_SENSOR_PIN 35    // Analog pin for moisture sensor
#define ACOUSTIC_SENSOR_PIN 32    // Analog pin for acoustic sensor

// Sensor calibration constants
#define PRESSURE_MIN 0.0
#define PRESSURE_MAX 100.0
#define MOISTURE_MIN 0.0
#define MOISTURE_MAX 100.0
#define ACOUSTIC_THRESHOLD 50.0

// Transmission interval (milliseconds)
#define TRANSMISSION_INTERVAL 5000

unsigned long lastTransmission = 0;
int packetCounter = 0;

struct SensorData {
  float pressure;      // PSI
  float moisture;      // Percentage
  float acoustic;      // dB level
  unsigned long timestamp;
};

void setup() {
  Serial.begin(115200);
  while (!Serial);
  
  Serial.println("LeakSense ESP32 Transmitter Starting...");
  
  // Configure sensor pins
  pinMode(PRESSURE_SENSOR_PIN, INPUT);
  pinMode(MOISTURE_SENSOR_PIN, INPUT);
  pinMode(ACOUSTIC_SENSOR_PIN, INPUT);
  
  // Initialize LoRa
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);
  
  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  
  // LoRa Configuration
  LoRa.setSpreadingFactor(7);           // SF7 to SF12
  LoRa.setSignalBandwidth(125E3);       // 125 kHz
  LoRa.setCodingRate4(5);               // 4/5
  LoRa.setSyncWord(0x12);               // Sync word
  LoRa.enableCrc();                     // Enable CRC
  
  Serial.println("LoRa initialized successfully!");
  Serial.println("Frequency: 915 MHz");
  Serial.println("Starting sensor readings...");
}

float readPressureSensor() {
  // Read analog value (0-4095 for ESP32 12-bit ADC)
  int rawValue = analogRead(PRESSURE_SENSOR_PIN);
  
  // Convert to pressure (0-100 PSI)
  // Assuming linear sensor output
  float pressure = map(rawValue, 0, 4095, PRESSURE_MIN * 10, PRESSURE_MAX * 10) / 10.0;
  
  // Add some realistic variation
  pressure += random(-5, 5) / 10.0;
  
  return constrain(pressure, PRESSURE_MIN, PRESSURE_MAX);
}

float readMoistureSensor() {
  // Read analog value
  int rawValue = analogRead(MOISTURE_SENSOR_PIN);
  
  // Convert to percentage (0-100%)
  // Lower value = more moisture (inverted for capacitive sensors)
  float moisture = map(rawValue, 0, 4095, 0, 1000) / 10.0;
  
  // Add some realistic variation
  moisture += random(-3, 3) / 10.0;
  
  return constrain(moisture, MOISTURE_MIN, MOISTURE_MAX);
}

float readAcousticSensor() {
  // Read analog value
  int rawValue = analogRead(ACOUSTIC_SENSOR_PIN);
  
  // Convert to dB level (approximate)
  // Typical range: 30-100 dB
  float acoustic = map(rawValue, 0, 4095, 300, 1000) / 10.0;
  
  // Add some realistic variation
  acoustic += random(-2, 2) / 10.0;
  
  return constrain(acoustic, 30.0, 100.0);
}

void transmitSensorData(SensorData data) {
  // Create JSON-like string for transmission
  String payload = "{";
  payload += "\"id\":" + String(packetCounter) + ",";
  payload += "\"pressure\":" + String(data.pressure, 2) + ",";
  payload += "\"moisture\":" + String(data.moisture, 2) + ",";
  payload += "\"acoustic\":" + String(data.acoustic, 2) + ",";
  payload += "\"timestamp\":" + String(data.timestamp);
  payload += "}";
  
  // Send LoRa packet
  LoRa.beginPacket();
  LoRa.print(payload);
  LoRa.endPacket();
  
  // Print to serial
  Serial.println("\n=== Packet #" + String(packetCounter) + " Transmitted ===");
  Serial.println("Pressure: " + String(data.pressure, 2) + " PSI");
  Serial.println("Moisture: " + String(data.moisture, 2) + " %");
  Serial.println("Acoustic: " + String(data.acoustic, 2) + " dB");
  Serial.println("Payload: " + payload);
  Serial.println("Payload Size: " + String(payload.length()) + " bytes");
  
  // Check for alerts
  if (data.moisture > 70.0) {
    Serial.println("⚠️  ALERT: High moisture detected!");
  }
  if (data.acoustic > 75.0) {
    Serial.println("⚠️  ALERT: High acoustic level detected!");
  }
  if (data.pressure < 20.0 || data.pressure > 80.0) {
    Serial.println("⚠️  ALERT: Abnormal pressure detected!");
  }
  
  packetCounter++;
}

void loop() {
  unsigned long currentTime = millis();
  
  // Transmit data at specified interval
  if (currentTime - lastTransmission >= TRANSMISSION_INTERVAL) {
    SensorData data;
    
    // Read all sensors
    data.pressure = readPressureSensor();
    data.moisture = readMoistureSensor();
    data.acoustic = readAcousticSensor();
    data.timestamp = currentTime;
    
    // Transmit via LoRa
    transmitSensorData(data);
    
    lastTransmission = currentTime;
  }
  
  // Small delay to prevent watchdog issues
  delay(10);
}
