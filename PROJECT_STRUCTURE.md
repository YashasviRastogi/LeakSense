# LeakSense Project Structure

## 📁 Complete Directory Tree

```
Leaksense/
│
├── 📄 README.md                    # Main project documentation
├── 📄 SETUP_GUIDE.md              # Complete setup instructions
├── 📄 QUICK_START.md              # 5-minute quick start guide
├── 📄 HARDWARE_GUIDE.md           # Hardware assembly guide
├── 📄 PROJECT_STRUCTURE.md        # This file
├── 📄 LICENSE                     # MIT License
├── 📄 .gitignore                  # Git ignore rules
│
├── 📁 esp32_transmitter/          # ESP32 sensor transmitter
│   ├── 📁 src/
│   │   └── 📄 main.cpp           # ESP32 main code
│   ├── 📄 platformio.ini         # PlatformIO configuration
│   └── 📄 README.md              # ESP32 setup guide
│
├── 📁 raspberry_pi_receiver/      # Raspberry Pi LoRa receiver
│   ├── 📄 lora_receiver.py       # LoRa reception & storage
│   ├── 📄 database.py            # Database interface
│   ├── 📄 requirements.txt       # Python dependencies
│   └── 📄 README.md              # Receiver setup guide
│
├── 📁 flask_backend/              # Flask REST API server
│   ├── 📄 app.py                 # Main Flask application
│   ├── 📄 config.py              # Configuration settings
│   ├── 📄 requirements.txt       # Python dependencies
│   └── 📄 README.md              # API documentation
│
├── 📁 web_frontend/               # Web dashboard
│   ├── 📄 index.html             # Main dashboard page
│   ├── 📁 css/
│   │   └── 📄 style.css          # Styles & animations
│   ├── 📁 js/
│   │   ├── 📄 app.js             # Main application logic
│   │   └── 📄 charts.js          # Chart configurations
│   └── 📄 README.md              # Frontend documentation
│
└── 📁 database/                   # Database setup
    ├── 📄 schema.sql             # PostgreSQL schema
    └── 📄 README.md              # Database documentation
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     LEAKSENSE SYSTEM                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   TRANSMITTER    │
│    (ESP32)       │
│                  │
│  ┌────────────┐  │
│  │ Pressure   │  │
│  │ Sensor     │──┤
│  └────────────┘  │
│                  │
│  ┌────────────┐  │
│  │ Moisture   │  │
│  │ Sensor     │──┤──> Read Sensors
│  └────────────┘  │
│                  │
│  ┌────────────┐  │
│  │ Acoustic   │  │
│  │ Sensor     │──┤
│  └────────────┘  │
│                  │
│  ┌────────────┐  │
│  │   LoRa     │  │
│  │ Transmit   │──┼──> Transmit via LoRa
│  └────────────┘  │    (915 MHz)
└──────────────────┘
         │
         │ LoRa Signal
         │ (JSON Payload)
         ▼
┌──────────────────┐
│    RECEIVER      │
│ (Raspberry Pi)   │
│                  │
│  ┌────────────┐  │
│  │   LoRa     │  │
│  │  Receive   │◄─┼─── Receive LoRa
│  └────────────┘  │
│         │        │
│         ▼        │
│  ┌────────────┐  │
│  │  Parse &   │  │
│  │  Validate  │  │
│  └────────────┘  │
│         │        │
│         ▼        │
│  ┌────────────┐  │
│  │ PostgreSQL │  │
│  │  Database  │◄─┼─── Store Data
│  └────────────┘  │
└──────────────────┘
         │
         │ SQL Queries
         ▼
┌──────────────────┐
│   FLASK API      │
│   (Backend)      │
│                  │
│  ┌────────────┐  │
│  │  REST API  │  │
│  │ Endpoints  │◄─┼─── Serve Data
│  └────────────┘  │
│         │        │
│         ▼        │
│  ┌────────────┐  │
│  │   JSON     │  │
│  │ Response   │  │
│  └────────────┘  │
└──────────────────┘
         │
         │ HTTP/JSON
         ▼
┌──────────────────┐
│  WEB DASHBOARD   │
│  (Frontend)      │
│                  │
│  ┌────────────┐  │
│  │  Real-time │  │
│  │   Gauges   │  │
│  └────────────┘  │
│                  │
│  ┌────────────┐  │
│  │ Interactive│  │
│  │   Charts   │  │
│  └────────────┘  │
│                  │
│  ┌────────────┐  │
│  │   Alerts   │  │
│  │  & Stats   │  │
│  └────────────┘  │
└──────────────────┘
         │
         ▼
    👤 USER
```

---

## 🔌 Component Interactions

### 1. ESP32 Transmitter
**Purpose**: Read sensors and transmit data via LoRa

**Key Files**:
- `main.cpp` - Sensor reading and LoRa transmission

**Dependencies**:
- LoRa library
- SPI library
- Arduino core

**Data Output**: JSON payload via LoRa
```json
{
  "id": 123,
  "pressure": 45.67,
  "moisture": 32.45,
  "acoustic": 55.30,
  "timestamp": 1234567890
}
```

---

### 2. Raspberry Pi Receiver
**Purpose**: Receive LoRa data and store in database

**Key Files**:
- `lora_receiver.py` - LoRa reception handler
- `database.py` - Database operations

**Dependencies**:
- pyLoRa
- psycopg2
- RPi.GPIO

**Data Flow**:
```
LoRa Signal → Parse JSON → Validate → Store in PostgreSQL
```

---

### 3. Flask Backend
**Purpose**: Provide REST API for data access

**Key Files**:
- `app.py` - API endpoints
- `config.py` - Configuration

**API Endpoints**:
```
GET /api/health              - Health check
GET /api/sensors/latest      - Latest reading
GET /api/sensors/recent      - Recent readings
GET /api/sensors/range       - Time range query
GET /api/sensors/statistics  - Statistical summary
GET /api/sensors/alerts      - Alert readings
GET /api/sensors/chart-data  - Chart data
```

---

### 4. Web Frontend
**Purpose**: Visualize sensor data with animations

**Key Files**:
- `index.html` - Dashboard structure
- `style.css` - Styling and animations
- `app.js` - Application logic
- `charts.js` - Chart configurations

**Features**:
- Real-time gauge charts
- Interactive line charts
- Alert notifications
- Statistics display

---

### 5. Database
**Purpose**: Store and manage sensor data

**Key Files**:
- `schema.sql` - Database schema

**Tables**:
- `sensor_readings` - Main data table

**Views**:
- `recent_readings` - Last 100 readings
- `hourly_averages` - Hourly aggregates
- `daily_statistics` - Daily stats
- `alert_readings` - Threshold violations

---

## 🔧 Configuration Files

### ESP32 Configuration
**File**: `esp32_transmitter/platformio.ini`
- Board settings
- Library dependencies
- Build flags

### Raspberry Pi Configuration
**File**: `raspberry_pi_receiver/requirements.txt`
- Python package dependencies

### Flask Configuration
**File**: `flask_backend/config.py`
- Database credentials
- Server settings
- CORS configuration

### Database Configuration
**File**: `database/schema.sql`
- Table definitions
- Indexes
- Views and functions

---

## 📊 Data Schema

### sensor_readings Table
```sql
CREATE TABLE sensor_readings (
    id          SERIAL PRIMARY KEY,
    pressure    REAL NOT NULL,
    moisture    REAL NOT NULL,
    acoustic    REAL NOT NULL,
    rssi        INTEGER,
    snr         REAL,
    timestamp   TIMESTAMP NOT NULL,
    created_at  TIMESTAMP NOT NULL
);
```

---

## 🚀 Deployment Architecture

### Development Setup
```
Local Machine
├── ESP32 (USB connected)
├── Raspberry Pi (SSH)
└── Web Browser (localhost:5000)
```

### Production Setup
```
Network
├── ESP32 Transmitter (Field deployment)
├── Raspberry Pi Receiver (Central location)
│   ├── PostgreSQL Database
│   ├── LoRa Receiver Service
│   └── Flask API Service
└── Clients (Web browsers, mobile apps)
```

---

## 🔐 Security Considerations

### Database
- Change default passwords
- Use SSL connections
- Restrict network access
- Regular backups

### API
- Implement authentication (JWT)
- Rate limiting
- HTTPS in production
- Input validation

### Hardware
- Secure physical access
- Encrypted LoRa (optional)
- VPN for remote access

---

## 📈 Scalability

### Horizontal Scaling
- Multiple ESP32 transmitters
- Load-balanced Flask instances
- Database replication

### Vertical Scaling
- Upgrade Raspberry Pi model
- Increase database resources
- Optimize queries

---

## 🧪 Testing Strategy

### Unit Tests
- Sensor reading functions
- Database operations
- API endpoints

### Integration Tests
- End-to-end data flow
- LoRa communication
- API responses

### System Tests
- Full system operation
- Performance testing
- Stress testing

---

## 📝 Development Workflow

1. **Modify Code**: Edit source files
2. **Test Locally**: Verify changes work
3. **Deploy**: Upload to hardware
4. **Monitor**: Check logs and metrics
5. **Iterate**: Refine and improve

---

## 🔄 Update Process

### ESP32 Firmware
```bash
cd esp32_transmitter
pio run --target upload
```

### Raspberry Pi Software
```bash
git pull
pip3 install -r requirements.txt
sudo systemctl restart leaksense-receiver
sudo systemctl restart leaksense-api
```

### Database Schema
```bash
psql -U leaksense_user -d leaksense < database/schema.sql
```

---

## 📚 Documentation Index

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Complete setup
- **QUICK_START.md** - Fast setup
- **HARDWARE_GUIDE.md** - Hardware details
- **PROJECT_STRUCTURE.md** - This file
- **Component READMEs** - Specific guides

---

## 🎯 Key Takeaways

1. **Modular Design**: Each component is independent
2. **Clear Interfaces**: Well-defined data formats
3. **Scalable**: Easy to add sensors or features
4. **Documented**: Comprehensive guides
5. **Production-Ready**: Systemd services, error handling

---

**Understanding the structure helps you navigate and modify the system effectively! 🚀**
