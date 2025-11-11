# LeakSense - IoT Sensor Monitoring System

## 🎯 Overview
LeakSense is a complete IoT-based sensor monitoring system that uses LoRa communication to transmit sensor data from ESP32 to a Raspberry Pi, stores it in PostgreSQL, and displays real-time animated visualizations on a web interface.

## 📚 Documentation

### 🚀 Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)** - Hardware assembly and BOM
- **[INDEX.md](INDEX.md)** - Complete documentation index

### 📖 Reference
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - REST API reference
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Architecture details
- **[SYSTEM_DIAGRAM.txt](SYSTEM_DIAGRAM.txt)** - Visual system diagrams
- **[SUMMARY.md](SUMMARY.md)** - Project completion summary

### 🔧 Component Guides
- **[ESP32 Transmitter](esp32_transmitter/README.md)** - ESP32 setup
- **[Raspberry Pi Receiver](raspberry_pi_receiver/README.md)** - RPi setup
- **[Flask Backend](flask_backend/README.md)** - API setup
- **[Web Frontend](web_frontend/README.md)** - Dashboard guide
- **[Database](database/README.md)** - Database setup

## 🏗️ System Architecture

### Hardware Components
- **Transmitter Side:**
  - ESP32 microcontroller
  - LoRa transmitter module (SX1276/SX1278)
  - Pressure sensor (0-100 PSI)
  - Moisture sensor (0-100%)
  - Acoustic sensor (30-100 dB)

- **Receiver Side:**
  - Raspberry Pi (3/4/Zero W)
  - LoRa receiver module (SX1276/SX1278)
  - PostgreSQL database

### Software Stack
- **ESP32:** C++ (Arduino/PlatformIO) with LoRa library
- **Raspberry Pi:** Python 3.8+ with LoRa library
- **Backend:** Flask REST API with 7 endpoints
- **Database:** PostgreSQL with optimized schema
- **Frontend:** HTML5, CSS3, JavaScript with Chart.js

## 📦 Project Structure
```
Leaksense/
├── 📚 Documentation
│   ├── README.md                  ← You are here
│   ├── QUICK_START.md            ← Start here for setup
│   ├── SETUP_GUIDE.md            ← Complete guide
│   ├── HARDWARE_GUIDE.md         ← Assembly instructions
│   ├── API_DOCUMENTATION.md      ← API reference
│   ├── PROJECT_STRUCTURE.md      ← Architecture
│   ├── SYSTEM_DIAGRAM.txt        ← Visual diagrams
│   ├── SUMMARY.md                ← Project summary
│   └── INDEX.md                  ← Documentation index
│
├── 🔧 esp32_transmitter/         ← ESP32 sensor code
│   ├── src/main.cpp              ← Main code
│   ├── platformio.ini            ← Build config
│   └── README.md
│
├── 🍓 raspberry_pi_receiver/     ← Raspberry Pi receiver
│   ├── lora_receiver.py          ← LoRa reception
│   ├── database.py               ← DB interface
│   ├── requirements.txt
│   └── README.md
│
├── 🌐 flask_backend/             ← Flask API server
│   ├── app.py                    ← REST API
│   ├── config.py                 ← Configuration
│   ├── requirements.txt
│   └── README.md
│
├── 🎨 web_frontend/              ← Web dashboard
│   ├── index.html                ← Dashboard
│   ├── css/style.css             ← Styles
│   ├── js/app.js                 ← Logic
│   ├── js/charts.js              ← Charts
│   └── README.md
│
└── 💾 database/                  ← Database setup
    ├── schema.sql                ← DB schema
    └── README.md
```

## ⚡ Quick Start

### Option 1: Fast Setup (5 minutes)
Follow **[QUICK_START.md](QUICK_START.md)** for rapid deployment

### Option 2: Complete Setup
Follow **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for detailed instructions

### Basic Steps:
```bash
# 1. Setup Database
sudo -u postgres psql < database/schema.sql

# 2. Upload ESP32 Code
cd esp32_transmitter && pio run --target upload

# 3. Start Raspberry Pi Receiver
cd raspberry_pi_receiver && python3 lora_receiver.py

# 4. Start Flask Backend
cd flask_backend && python3 app.py

# 5. Access Dashboard
# Open browser: http://localhost:5000
```

## ✨ Features

### Data Collection & Transmission
- ✅ Real-time sensor data transmission via LoRa (2-10km range)
- ✅ 915 MHz frequency (configurable)
- ✅ JSON payload format
- ✅ 5-second transmission interval
- ✅ RSSI/SNR signal monitoring

### Data Storage & Processing
- ✅ PostgreSQL database with optimized indexes
- ✅ Automatic timestamp recording
- ✅ Statistical views and functions
- ✅ Data cleanup utilities

### Web Dashboard
- ✅ Animated, responsive design
- ✅ Real-time gauge charts
- ✅ Interactive line charts
- ✅ Time range selection (1h, 6h, 24h)
- ✅ Live data updates every 5 seconds
- ✅ Alert notifications
- ✅ Statistics display
- ✅ Mobile-friendly navigation
- ✅ Multi-page interface

#### Frontend Pages
1. **Dashboard** - Real-time sensor monitoring with animated gauges and charts
2. **Report Issue** - Community reporting system for quick issue identification
3. **Community Leaderboard** - Gamified system with points, badges, and prizes

### REST API
- ✅ 7 RESTful endpoints
- ✅ JSON responses
- ✅ CORS enabled
- ✅ Health monitoring
- ✅ Statistical analysis

### Alerting System
- ✅ High moisture detection (>70%)
- ✅ High acoustic level (>75 dB)
- ✅ Abnormal pressure (<20 or >80 PSI)
- ✅ Visual notifications
- ✅ Alert history

## 🔌 Sensor Details
- **Pressure Sensor:** Water pressure monitoring (0-100 PSI)
- **Moisture Sensor:** Leak detection (0-100%)
- **Acoustic Sensor:** Sound level detection (30-100 dB)

## 📱 Frontend Pages

### 1. Dashboard Page
The main monitoring interface featuring:
- **Real-time Gauges**: Animated circular gauges for pressure, moisture, and acoustic sensors
- **Live Charts**: Interactive multi-axis line chart with time range selection
- **Statistics Cards**: Min/Max/Average values for each sensor
- **Alert Banner**: Visual notifications for threshold breaches
- **Info Cards**: Total readings, last update, signal strength, active alerts

### 2. Report Issue Page
Community-driven issue reporting system:
- **Report Form**: Easy-to-use form with fields for:
  - Issue Type (leak, pressure, moisture, acoustic, sensor malfunction, other)
  - Location (building, floor, room)
  - Severity Level (low, medium, high, critical)
  - Detailed Description
  - Reporter Name & Contact
- **Recent Reports**: Live feed of latest community reports
- **Quick Submit**: Mobile-optimized for fast reporting on-the-go

### 3. Community Leaderboard Page
Gamified engagement system to encourage participation:

**Leaderboard Features:**
- **Top Contributors Table**: Ranked list showing:
  - User rankings with gold/silver/bronze badges
  - Total reports submitted
  - Points earned
  - Achievement badges
- **Statistics Dashboard**:
  - Total community reports
  - Fastest response time
  - Issues resolved count
- **Achievements & Badges**:
  - 🥇 **First Reporter** - First to report an issue (+50 pts)
  - ⚡ **Speed Demon** - Report within 5 minutes (+30 pts)
  - 🔥 **Hot Streak** - 5 reports in a week (+100 pts)
  - 🎯 **Accurate Reporter** - 10 verified reports (+150 pts)
  - 👑 **Community Hero** - Top contributor of the month (+500 pts)
  - 💎 **Diamond Status** - 1000+ total points (Legendary)
- **Monthly Prizes**:
  - 🥇 **1st Place**: $100 Gift Card + Premium Badge
  - 🥈 **2nd Place**: $50 Gift Card + Silver Badge
  - 🥉 **3rd Place**: $25 Gift Card + Bronze Badge

**Points System:**
- Low severity report: 10 points
- Medium severity report: 25 points
- High severity report: 50 points
- Critical severity report: 100 points
- Bonus points for speed and accuracy

## 🌐 API Endpoints
```
GET  /api/health                 Health check
GET  /api/sensors/latest         Latest reading
GET  /api/sensors/recent         Recent readings
GET  /api/sensors/range          Time range query
GET  /api/sensors/statistics     Statistical summary
GET  /api/sensors/alerts         Alert readings
GET  /api/sensors/chart-data     Chart data
```

**Full API Documentation:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🛠️ Hardware Requirements

### Transmitter (ESP32)
- ESP32 development board
- LoRa SX1276/SX1278 module
- Pressure, moisture, and acoustic sensors
- Breadboard and jumper wires
- 5V power supply

### Receiver (Raspberry Pi)
- Raspberry Pi 3/4/Zero W
- LoRa SX1276/SX1278 module
- MicroSD card (16GB+)
- 5V 3A power supply

**Complete BOM:** [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)

## 📊 Technical Specifications
- **Range:** 2-10 km (line of sight)
- **Frequency:** 915 MHz (configurable: 433/868/915 MHz)
- **Transmission Rate:** Every 5 seconds
- **API Response Time:** <100ms
- **Database:** PostgreSQL 12+
- **Python:** 3.8+
- **Web Browser:** Chrome 90+, Firefox 88+, Safari 14+

## 🎓 Learning Outcomes
This project demonstrates:
- Complete IoT sensor-to-cloud pipeline
- LoRa long-range wireless communication
- PostgreSQL database design and optimization
- REST API development with Flask
- Modern web development with animations
- System integration and deployment

## 🚀 Deployment
- **Development:** Local setup with USB connections
- **Production:** Systemd services for auto-start
- **Monitoring:** Logs via journalctl
- **Backup:** Database backup scripts included

## 🔐 Security
- Database password protection
- CORS configuration
- Input validation
- Error handling
- Production deployment guidelines

## 🆘 Support
- **Troubleshooting:** See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)
- **Hardware Issues:** See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md#troubleshooting)
- **API Reference:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Component Guides:** Check individual README files

## 📈 Future Enhancements
- Email/SMS notifications
- Mobile app
- Machine learning anomaly detection
- Cloud deployment (AWS/Azure)
- Multi-transmitter support
- Advanced analytics

## 📄 License
MIT License - See [LICENSE](LICENSE) file

## 🎉 Ready to Start?
1. **Quick Setup:** Follow [QUICK_START.md](QUICK_START.md)
2. **Complete Guide:** Follow [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. **Hardware Assembly:** See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)

**Happy Monitoring! 🚀**
