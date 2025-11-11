# 📑 LeakSense Complete Index

## Quick Navigation

### 🚀 Getting Started
- **[README.md](README.md)** - Project overview and introduction
- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[SUMMARY.md](SUMMARY.md)** - Project completion summary

### 📖 Documentation
- **[HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)** - Hardware assembly and BOM
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - REST API reference
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Architecture details
- **[SYSTEM_DIAGRAM.txt](SYSTEM_DIAGRAM.txt)** - Visual system diagrams

### 🔧 Component Guides
- **[esp32_transmitter/README.md](esp32_transmitter/README.md)** - ESP32 setup
- **[raspberry_pi_receiver/README.md](raspberry_pi_receiver/README.md)** - RPi setup
- **[flask_backend/README.md](flask_backend/README.md)** - Flask API setup
- **[web_frontend/README.md](web_frontend/README.md)** - Frontend guide
- **[database/README.md](database/README.md)** - Database setup

---

## 📂 File Directory

### Root Level Files
```
├── README.md                    Main project documentation
├── QUICK_START.md              5-minute quick start guide
├── SETUP_GUIDE.md              Complete setup instructions
├── HARDWARE_GUIDE.md           Hardware assembly guide
├── API_DOCUMENTATION.md        REST API reference
├── PROJECT_STRUCTURE.md        Architecture and structure
├── SUMMARY.md                  Project summary
├── SYSTEM_DIAGRAM.txt          Visual diagrams
├── INDEX.md                    This file
├── LICENSE                     MIT License
└── .gitignore                  Git ignore rules
```

### ESP32 Transmitter
```
esp32_transmitter/
├── src/
│   └── main.cpp                ESP32 main code (sensors + LoRa)
├── platformio.ini              PlatformIO configuration
└── README.md                   ESP32 setup guide
```

### Raspberry Pi Receiver
```
raspberry_pi_receiver/
├── lora_receiver.py            LoRa reception and storage
├── database.py                 PostgreSQL interface
├── requirements.txt            Python dependencies
└── README.md                   Receiver setup guide
```

### Flask Backend
```
flask_backend/
├── app.py                      Flask REST API server
├── config.py                   Configuration settings
├── requirements.txt            Python dependencies
└── README.md                   API documentation
```

### Web Frontend
```
web_frontend/
├── index.html                  Main dashboard page
├── css/
│   └── style.css              Styles and animations
├── js/
│   ├── app.js                 Application logic
│   └── charts.js              Chart configurations
└── README.md                   Frontend documentation
```

### Database
```
database/
├── schema.sql                  PostgreSQL schema
└── README.md                   Database documentation
```

---

## 🎯 Use Case Index

### I want to...

#### Set up the system quickly
→ **[QUICK_START.md](QUICK_START.md)**

#### Understand the complete setup process
→ **[SETUP_GUIDE.md](SETUP_GUIDE.md)**

#### Assemble the hardware
→ **[HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)**

#### Understand the system architecture
→ **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**
→ **[SYSTEM_DIAGRAM.txt](SYSTEM_DIAGRAM.txt)**

#### Use the API
→ **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

#### Modify the ESP32 code
→ **[esp32_transmitter/src/main.cpp](esp32_transmitter/src/main.cpp)**
→ **[esp32_transmitter/README.md](esp32_transmitter/README.md)**

#### Configure the receiver
→ **[raspberry_pi_receiver/lora_receiver.py](raspberry_pi_receiver/lora_receiver.py)**
→ **[raspberry_pi_receiver/README.md](raspberry_pi_receiver/README.md)**

#### Customize the web interface
→ **[web_frontend/index.html](web_frontend/index.html)**
→ **[web_frontend/css/style.css](web_frontend/css/style.css)**
→ **[web_frontend/js/app.js](web_frontend/js/app.js)**

#### Work with the database
→ **[database/schema.sql](database/schema.sql)**
→ **[database/README.md](database/README.md)**

#### Troubleshoot issues
→ **[SETUP_GUIDE.md](SETUP_GUIDE.md)** (Troubleshooting section)
→ Component-specific README files

---

## 📚 Documentation by Topic

### Hardware
- **Bill of Materials**: [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#bill-of-materials)
- **Sensor Specs**: [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#sensor-specifications)
- **Wiring Diagrams**: [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#wiring-diagrams)
- **Assembly Instructions**: [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#assembly-instructions)
- **Power Requirements**: [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#power-considerations)

### Software - ESP32
- **Main Code**: [esp32_transmitter/src/main.cpp](esp32_transmitter/src/main.cpp)
- **Configuration**: [esp32_transmitter/platformio.ini](esp32_transmitter/platformio.ini)
- **Setup Guide**: [esp32_transmitter/README.md](esp32_transmitter/README.md)
- **Pin Definitions**: [esp32_transmitter/src/main.cpp](esp32_transmitter/src/main.cpp) (lines 10-18)

### Software - Raspberry Pi
- **LoRa Receiver**: [raspberry_pi_receiver/lora_receiver.py](raspberry_pi_receiver/lora_receiver.py)
- **Database Interface**: [raspberry_pi_receiver/database.py](raspberry_pi_receiver/database.py)
- **Setup Guide**: [raspberry_pi_receiver/README.md](raspberry_pi_receiver/README.md)
- **Dependencies**: [raspberry_pi_receiver/requirements.txt](raspberry_pi_receiver/requirements.txt)

### Software - Backend
- **Flask API**: [flask_backend/app.py](flask_backend/app.py)
- **Configuration**: [flask_backend/config.py](flask_backend/config.py)
- **API Endpoints**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Setup Guide**: [flask_backend/README.md](flask_backend/README.md)

### Software - Frontend
- **Dashboard HTML**: [web_frontend/index.html](web_frontend/index.html)
- **Styles**: [web_frontend/css/style.css](web_frontend/css/style.css)
- **Application Logic**: [web_frontend/js/app.js](web_frontend/js/app.js)
- **Charts**: [web_frontend/js/charts.js](web_frontend/js/charts.js)
- **Setup Guide**: [web_frontend/README.md](web_frontend/README.md)

### Database
- **Schema**: [database/schema.sql](database/schema.sql)
- **Setup Guide**: [database/README.md](database/README.md)
- **Queries**: [database/README.md](database/README.md#queries)
- **Maintenance**: [database/README.md](database/README.md#maintenance)

---

## 🔍 Code Reference Index

### Key Functions

#### ESP32 (main.cpp)
- `setup()` - Initialize hardware
- `loop()` - Main program loop
- `readPressureSensor()` - Read pressure sensor
- `readMoistureSensor()` - Read moisture sensor
- `readAcousticSensor()` - Read acoustic sensor
- `transmitSensorData()` - Transmit via LoRa

#### Raspberry Pi (lora_receiver.py)
- `LoRaReceiver.start()` - Start receiving
- `LoRaReceiver.on_rx_done()` - Handle received packet

#### Raspberry Pi (database.py)
- `Database.connect()` - Connect to database
- `Database.insert_sensor_data()` - Insert reading
- `Database.get_latest_readings()` - Get recent data
- `Database.get_statistics()` - Get statistics

#### Flask (app.py)
- `health_check()` - Health endpoint
- `get_latest_reading()` - Latest data endpoint
- `get_recent_readings()` - Recent data endpoint
- `get_statistics()` - Statistics endpoint
- `get_alerts()` - Alerts endpoint

#### Frontend (app.js)
- `fetchLatestData()` - Fetch latest reading
- `fetchStatistics()` - Fetch statistics
- `updateSensorValues()` - Update display
- `checkAlerts()` - Check for alerts

#### Frontend (charts.js)
- `initializeGauges()` - Create gauge charts
- `updateGauge()` - Update gauge values
- `initializeChart()` - Create line chart
- `updateMainChart()` - Update chart data

---

## 📊 API Endpoint Index

### Available Endpoints
```
GET  /api/health                 Health check
GET  /api/sensors/latest         Latest reading
GET  /api/sensors/recent         Recent readings
GET  /api/sensors/range          Time range query
GET  /api/sensors/statistics     Statistical summary
GET  /api/sensors/alerts         Alert readings
GET  /api/sensors/chart-data     Chart data
```

**Full Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🗄️ Database Schema Index

### Tables
- **sensor_readings** - Main data table

### Views
- **recent_readings** - Last 100 readings
- **hourly_averages** - Hourly statistics
- **daily_statistics** - Daily statistics
- **alert_readings** - Threshold violations

### Functions
- **cleanup_old_data()** - Delete old records
- **get_sensor_stats()** - Get statistics

**Full Schema**: [database/schema.sql](database/schema.sql)

---

## 🎨 Configuration Index

### ESP32 Configuration
**File**: [esp32_transmitter/platformio.ini](esp32_transmitter/platformio.ini)
- Board: ESP32 Dev Module
- Framework: Arduino
- Libraries: LoRa, Adafruit Sensors

**Code Configuration**: [esp32_transmitter/src/main.cpp](esp32_transmitter/src/main.cpp)
- LoRa Frequency: Line 14
- Pin Definitions: Lines 10-18
- Transmission Interval: Line 29

### Raspberry Pi Configuration
**File**: [raspberry_pi_receiver/lora_receiver.py](raspberry_pi_receiver/lora_receiver.py)
- LoRa Frequency: Line 13
- Spreading Factor: Line 14
- Bandwidth: Line 15

**Database Config**: [raspberry_pi_receiver/database.py](raspberry_pi_receiver/database.py)
- Connection settings: Lines 11-17

### Flask Configuration
**File**: [flask_backend/config.py](flask_backend/config.py)
- Database credentials
- Server settings
- CORS configuration

### Frontend Configuration
**File**: [web_frontend/js/app.js](web_frontend/js/app.js)
- API Base URL: Line 4
- Update Intervals: Lines 5-6
- Thresholds: Lines 9-13

---

## 🛠️ Troubleshooting Index

### Common Issues

#### ESP32 Issues
→ [SETUP_GUIDE.md - ESP32 Troubleshooting](SETUP_GUIDE.md#esp32-issues)
→ [esp32_transmitter/README.md - Troubleshooting](esp32_transmitter/README.md#troubleshooting)

#### Raspberry Pi Issues
→ [SETUP_GUIDE.md - Raspberry Pi Troubleshooting](SETUP_GUIDE.md#raspberry-pi-issues)
→ [raspberry_pi_receiver/README.md - Troubleshooting](raspberry_pi_receiver/README.md#troubleshooting)

#### Web Dashboard Issues
→ [SETUP_GUIDE.md - Web Dashboard Troubleshooting](SETUP_GUIDE.md#web-dashboard-issues)
→ [web_frontend/README.md - Troubleshooting](web_frontend/README.md#troubleshooting)

#### Database Issues
→ [database/README.md - Troubleshooting](database/README.md#troubleshooting)

---

## 📈 Performance Optimization Index

### ESP32 Optimization
- Adjust transmission interval
- Optimize sensor reading frequency
- Power management settings

### Database Optimization
- Index optimization: [database/schema.sql](database/schema.sql)
- Query optimization: [database/README.md](database/README.md#performance-tips)
- Data cleanup: [database/README.md](database/README.md#maintenance)

### Frontend Optimization
- Chart data point limiting: [web_frontend/js/charts.js](web_frontend/js/charts.js)
- Update interval tuning: [web_frontend/js/app.js](web_frontend/js/app.js)

---

## 🔐 Security Index

### Database Security
→ [database/README.md - Security](database/README.md#security)

### API Security
→ [flask_backend/README.md - Security](flask_backend/README.md#security)

### Hardware Security
→ [HARDWARE_GUIDE.md - Safety Guidelines](HARDWARE_GUIDE.md#safety-guidelines)

---

## 📦 Dependencies Index

### ESP32 Dependencies
**File**: [esp32_transmitter/platformio.ini](esp32_transmitter/platformio.ini)
- LoRa library
- Adafruit Unified Sensor
- Adafruit BMP280

### Raspberry Pi Dependencies
**File**: [raspberry_pi_receiver/requirements.txt](raspberry_pi_receiver/requirements.txt)
- psycopg2-binary
- RPi.GPIO
- spidev
- pyLoRa

### Flask Dependencies
**File**: [flask_backend/requirements.txt](flask_backend/requirements.txt)
- Flask
- Flask-CORS
- psycopg2-binary
- python-dotenv

### Frontend Dependencies
- Chart.js (CDN)
- Google Fonts (CDN)

---

## 🎓 Learning Resources Index

### ESP32 Resources
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [LoRa Library](https://github.com/sandeepmistry/arduino-LoRa)

### Raspberry Pi Resources
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [GPIO Pinout](https://pinout.xyz/)

### Flask Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)

### PostgreSQL Resources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

### Frontend Resources
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## 🚀 Deployment Checklist

**Complete Checklist**: [SYSTEM_DIAGRAM.txt](SYSTEM_DIAGRAM.txt#deployment-checklist)

Quick Links:
- ESP32 Setup: [SETUP_GUIDE.md - Part 1](SETUP_GUIDE.md#part-1-esp32-transmitter-setup)
- Raspberry Pi Setup: [SETUP_GUIDE.md - Part 2](SETUP_GUIDE.md#part-2-raspberry-pi-receiver-setup)
- Flask Setup: [SETUP_GUIDE.md - Part 3](SETUP_GUIDE.md#part-3-flask-backend-setup)
- Testing: [SETUP_GUIDE.md - Testing](SETUP_GUIDE.md#testing-the-complete-system)

---

## 📞 Quick Reference

### Important Files
- **Start Here**: [README.md](README.md)
- **Quick Setup**: [QUICK_START.md](QUICK_START.md)
- **Main Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **API Reference**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Key Code Files
- **ESP32**: [esp32_transmitter/src/main.cpp](esp32_transmitter/src/main.cpp)
- **Receiver**: [raspberry_pi_receiver/lora_receiver.py](raspberry_pi_receiver/lora_receiver.py)
- **API**: [flask_backend/app.py](flask_backend/app.py)
- **Frontend**: [web_frontend/index.html](web_frontend/index.html)
- **Database**: [database/schema.sql](database/schema.sql)

### Configuration Files
- **ESP32**: [esp32_transmitter/platformio.ini](esp32_transmitter/platformio.ini)
- **Flask**: [flask_backend/config.py](flask_backend/config.py)
- **Frontend**: [web_frontend/js/app.js](web_frontend/js/app.js) (lines 4-13)

---

## 🎉 You're Ready!

Everything you need is documented and indexed. Start with:
1. **[QUICK_START.md](QUICK_START.md)** for rapid deployment
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for detailed instructions
3. **[HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)** for assembly

**Happy Building! 🚀**
