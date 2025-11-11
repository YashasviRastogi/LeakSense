# LeakSense Hardware Guide

## 📦 Bill of Materials (BOM)

### Transmitter Side (ESP32)

| Component | Quantity | Specifications | Estimated Cost |
|-----------|----------|----------------|----------------|
| ESP32 Dev Board | 1 | ESP32-WROOM-32 | $8-12 |
| LoRa Module | 1 | SX1276/SX1278 (915MHz) | $10-15 |
| Pressure Sensor | 1 | 0-100 PSI, Analog output | $15-25 |
| Moisture Sensor | 1 | Capacitive or Resistive | $3-8 |
| Acoustic Sensor | 1 | MAX4466 or similar | $5-10 |
| Breadboard | 1 | 830 points | $3-5 |
| Jumper Wires | 1 set | Male-to-Male, Male-to-Female | $3-5 |
| Power Supply | 1 | 5V 2A USB or battery | $5-10 |
| Antenna | 1 | 915MHz (or matching frequency) | $2-5 |
| **Total** | | | **~$54-95** |

### Receiver Side (Raspberry Pi)

| Component | Quantity | Specifications | Estimated Cost |
|-----------|----------|----------------|----------------|
| Raspberry Pi | 1 | Pi 3B+/4B (2GB+) | $35-55 |
| LoRa Module | 1 | SX1276/SX1278 (915MHz) | $10-15 |
| MicroSD Card | 1 | 16GB+ Class 10 | $8-12 |
| Power Supply | 1 | 5V 3A USB-C | $8-12 |
| Antenna | 1 | 915MHz (or matching frequency) | $2-5 |
| Case (Optional) | 1 | Raspberry Pi case | $5-10 |
| **Total** | | | **~$68-109** |

### Optional Components

| Component | Purpose | Cost |
|-----------|---------|------|
| Enclosures | Weather protection | $10-20 |
| Heat sinks | Cooling | $3-5 |
| UPS/Battery | Backup power | $20-50 |
| Ethernet Cable | Stable connection | $5-10 |

---

## 🔌 Sensor Specifications

### 1. Pressure Sensor

**Recommended Models:**
- **Analog Pressure Transducer** (0-100 PSI)
- **MPX5700AP** (0-100 kPa)
- **BMP280** (Digital, I2C)

**Specifications:**
- Operating Voltage: 3.3V or 5V
- Output: 0-3.3V analog or I2C digital
- Accuracy: ±1-2%
- Response Time: <10ms

**Wiring:**
```
VCC → 3.3V or 5V
GND → GND
OUT → ESP32 GPIO 34 (ADC)
```

### 2. Moisture Sensor

**Recommended Models:**
- **Capacitive Soil Moisture Sensor v1.2**
- **Resistive Moisture Sensor**
- **DHT22** (for humidity)

**Specifications:**
- Operating Voltage: 3.3V-5V
- Output: Analog (0-3.3V)
- Detection Range: 0-100%
- Corrosion Resistant: Yes (capacitive)

**Wiring:**
```
VCC → 3.3V
GND → GND
AOUT → ESP32 GPIO 35 (ADC)
```

### 3. Acoustic Sensor

**Recommended Models:**
- **MAX4466 Electret Microphone Amplifier**
- **MAX9814 Auto-Gain Microphone**
- **LM393 Sound Detection Module**

**Specifications:**
- Operating Voltage: 2.4V-5V
- Output: Analog (0-3.3V)
- Frequency Range: 20Hz-20kHz
- Gain: Adjustable

**Wiring:**
```
VCC → 3.3V
GND → GND
OUT → ESP32 GPIO 32 (ADC)
```

---

## 📡 LoRa Module Details

### SX1276/SX1278 LoRa Module

**Specifications:**
- Frequency: 433MHz, 868MHz, or 915MHz
- Transmission Power: Up to +20dBm
- Receiver Sensitivity: -148dBm
- Range: 2-10km (line of sight)
- Interface: SPI
- Operating Voltage: 3.3V

**Pin Configuration:**
```
VCC  → 3.3V (IMPORTANT: Not 5V!)
GND  → Ground
MISO → SPI MISO
MOSI → SPI MOSI
SCK  → SPI Clock
NSS  → Chip Select
RST  → Reset
DIO0 → Interrupt
```

**Antenna:**
- Use proper 915MHz antenna (or matching frequency)
- Length: ~8.2cm for 915MHz
- Type: Wire, helical, or PCB antenna
- Connection: U.FL or SMA connector

---

## 🔧 Assembly Instructions

### ESP32 Transmitter Assembly

#### Step 1: Prepare Components
- Lay out all components
- Check for damage
- Test continuity with multimeter

#### Step 2: Connect LoRa Module
1. Insert ESP32 into breadboard
2. Connect LoRa module using jumper wires
3. **CRITICAL**: Use 3.3V, NOT 5V!
4. Attach antenna to LoRa module

#### Step 3: Connect Sensors
1. Connect pressure sensor to GPIO 34
2. Connect moisture sensor to GPIO 35
3. Connect acoustic sensor to GPIO 32
4. Ensure common ground for all components

#### Step 4: Power Supply
- Use 5V 2A power supply via USB
- Or use battery pack (3.7V LiPo with regulator)

#### Step 5: Testing
1. Upload test code
2. Verify sensor readings
3. Check LoRa transmission

### Raspberry Pi Receiver Assembly

#### Step 1: Prepare Raspberry Pi
1. Flash Raspberry Pi OS to microSD
2. Insert microSD card
3. Connect keyboard, mouse, monitor

#### Step 2: Connect LoRa Module
1. Power off Raspberry Pi
2. Connect LoRa module to GPIO pins
3. **CRITICAL**: Use 3.3V, NOT 5V!
4. Attach antenna

#### Step 3: Initial Boot
1. Power on Raspberry Pi
2. Complete OS setup
3. Enable SPI interface

#### Step 4: Testing
1. Install software
2. Run receiver script
3. Verify data reception

---

## ⚡ Power Considerations

### ESP32 Power Requirements
- Operating Voltage: 3.3V (regulated from 5V USB)
- Current Draw: 80-240mA (varies with WiFi/LoRa usage)
- Peak Current: Up to 500mA
- Recommended: 5V 2A power supply

### Raspberry Pi Power Requirements
- Operating Voltage: 5V
- Current Draw: 500mA-1.2A (Pi 3B+)
- Current Draw: 600mA-1.5A (Pi 4B)
- Recommended: 5V 3A power supply

### Battery Operation

**ESP32 Battery Setup:**
- Use 3.7V LiPo battery (2000-5000mAh)
- Add TP4056 charging module
- Add voltage regulator (3.3V)
- Expected runtime: 8-24 hours (depending on capacity)

**Raspberry Pi Battery Setup:**
- Use 5V power bank (10000mAh+)
- Or use UPS HAT module
- Expected runtime: 4-12 hours

---

## 🌡️ Environmental Considerations

### Operating Temperature
- ESP32: -40°C to +85°C
- Raspberry Pi: 0°C to +50°C
- Sensors: Check individual specs

### Weatherproofing
1. Use IP65+ rated enclosures
2. Add silica gel packets for moisture
3. Use cable glands for wire entry
4. Apply conformal coating to PCBs

### Mounting
- Mount transmitter near sensors
- Keep antennas vertical
- Avoid metal enclosures (blocks signal)
- Ensure ventilation for heat dissipation

---

## 🔍 Testing & Calibration

### Sensor Calibration

**Pressure Sensor:**
1. Connect to known pressure source
2. Record readings at multiple pressures
3. Create calibration curve
4. Update code with correction factors

**Moisture Sensor:**
1. Test in dry condition (0%)
2. Test in water (100%)
3. Calculate scaling factors
4. Update code accordingly

**Acoustic Sensor:**
1. Test in quiet environment (baseline)
2. Test with known sound sources
3. Adjust gain if needed
4. Set threshold values

### LoRa Range Testing
1. Start with transmitter and receiver close
2. Gradually increase distance
3. Monitor RSSI and SNR values
4. Note maximum reliable range
5. Document dead zones

---

## 🛡️ Safety Guidelines

### Electrical Safety
- ⚠️ Never connect 5V to 3.3V pins
- ⚠️ Check polarity before powering on
- ⚠️ Use proper fuses for battery operation
- ⚠️ Avoid short circuits

### Handling
- Use ESD protection when handling components
- Avoid touching component pins
- Store in anti-static bags when not in use

### Installation
- Ensure proper ventilation
- Keep away from water (unless waterproofed)
- Secure all connections
- Label all wires

---

## 🔧 Maintenance

### Regular Checks
- **Weekly**: Check sensor readings for anomalies
- **Monthly**: Clean sensors, check connections
- **Quarterly**: Recalibrate sensors, update firmware
- **Yearly**: Replace batteries, check enclosures

### Troubleshooting Tools
- Multimeter (voltage, continuity)
- Logic analyzer (SPI debugging)
- Oscilloscope (signal analysis)
- Spectrum analyzer (LoRa frequency check)

---

## 📐 Wiring Diagrams

### ESP32 Complete Wiring
```
ESP32                    LoRa Module
-----                    -----------
3.3V -----------------> VCC
GND  -----------------> GND
GPIO 5  (SCK)  -------> SCK
GPIO 19 (MISO) -------> MISO
GPIO 27 (MOSI) -------> MOSI
GPIO 18 (CS)   -------> NSS
GPIO 14 (RST)  -------> RST
GPIO 26 (DIO0) -------> DIO0

ESP32                    Sensors
-----                    -------
GPIO 34 --------------> Pressure Sensor OUT
GPIO 35 --------------> Moisture Sensor OUT
GPIO 32 --------------> Acoustic Sensor OUT
3.3V -----------------> Sensor VCC (all)
GND  -----------------> Sensor GND (all)
```

### Raspberry Pi Complete Wiring
```
Raspberry Pi             LoRa Module
------------             -----------
Pin 1  (3.3V)  --------> VCC
Pin 6  (GND)   --------> GND
Pin 23 (GPIO 11) ------> SCK
Pin 21 (GPIO 9)  ------> MISO
Pin 19 (GPIO 10) ------> MOSI
Pin 24 (GPIO 8)  ------> NSS
Pin 22 (GPIO 25) ------> RST
Pin 7  (GPIO 4)  ------> DIO0
```

---

## 🛒 Where to Buy

### Online Retailers
- **Amazon**: Wide selection, fast shipping
- **AliExpress**: Budget-friendly, longer shipping
- **Adafruit**: Quality components, tutorials
- **SparkFun**: Reliable, good documentation
- **Digi-Key**: Professional components
- **Mouser**: Electronic components

### Local Options
- Electronics hobby stores
- Maker spaces
- University surplus stores

---

## 💡 Tips & Best Practices

1. **Always use 3.3V for LoRa modules** - 5V will damage them!
2. **Use quality jumper wires** - Poor connections cause intermittent issues
3. **Add decoupling capacitors** - 100nF near power pins for stability
4. **Keep wires short** - Reduces noise and interference
5. **Test components individually** - Easier to debug
6. **Document your setup** - Take photos, label wires
7. **Use proper antennas** - Wire antennas work but proper antennas are better
8. **Consider heat dissipation** - Add heat sinks if needed
9. **Secure connections** - Use hot glue or terminal blocks
10. **Plan for maintenance** - Make components accessible

---

## 📸 Reference Images

*Note: Add actual photos of your setup here*

- ESP32 with LoRa module connected
- Sensor connections
- Raspberry Pi with LoRa receiver
- Complete system in enclosure
- Antenna placement

---

## 🔗 Additional Resources

- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [Raspberry Pi Pinout](https://pinout.xyz/)
- [LoRa Calculator](https://www.rfwireless-world.com/calculators/LoRa-Data-Rate-Calculator.html)
- [Sensor Calibration Guide](https://learn.adafruit.com/calibrating-sensors)

---

**Good luck with your build! 🚀**
