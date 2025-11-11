# ESP32 LoRa Transmitter

## Hardware Requirements
- ESP32 Development Board
- LoRa SX1276/SX1278 Module
- Pressure Sensor (0-5V analog output)
- Moisture Sensor (capacitive or resistive)
- Acoustic Sensor (analog microphone module)
- Jumper wires and breadboard

## Pin Connections

### LoRa Module to ESP32
| LoRa Pin | ESP32 Pin |
|----------|-----------|
| VCC      | 3.3V      |
| GND      | GND       |
| SCK      | GPIO 5    |
| MISO     | GPIO 19   |
| MOSI     | GPIO 27   |
| NSS/CS   | GPIO 18   |
| RST      | GPIO 14   |
| DIO0     | GPIO 26   |

### Sensors to ESP32
| Sensor          | ESP32 Pin |
|-----------------|-----------|
| Pressure Sensor | GPIO 34   |
| Moisture Sensor | GPIO 35   |
| Acoustic Sensor | GPIO 32   |

## Installation

### Using PlatformIO (Recommended)
```bash
# Install PlatformIO
pip install platformio

# Navigate to project directory
cd esp32_transmitter

# Build and upload
pio run --target upload

# Monitor serial output
pio device monitor
```

### Using Arduino IDE
1. Install ESP32 board support
2. Install LoRa library by Sandeep Mistry
3. Open `src/main.cpp`
4. Select board: "ESP32 Dev Module"
5. Upload to ESP32

## Configuration

### LoRa Frequency
Modify in `main.cpp`:
```cpp
#define LORA_FREQUENCY 915E6  // 915 MHz (US)
// or 868E6 for EU
// or 433E6 for Asia
```

### Transmission Interval
```cpp
#define TRANSMISSION_INTERVAL 5000  // 5 seconds
```

## Data Format
Transmitted JSON payload:
```json
{
  "id": 123,
  "pressure": 45.67,
  "moisture": 23.45,
  "acoustic": 52.30,
  "timestamp": 1234567890
}
```

## Troubleshooting
- **LoRa initialization failed:** Check wiring and power supply
- **No sensor readings:** Verify sensor connections and power
- **Transmission issues:** Check LoRa frequency matches receiver
