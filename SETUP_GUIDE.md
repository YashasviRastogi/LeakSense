# LeakSense Complete Setup Guide

## 🎯 Overview
This guide will walk you through setting up the complete LeakSense IoT sensor monitoring system from scratch.

## 📋 Prerequisites

### Hardware
- ✅ ESP32 development board
- ✅ LoRa SX1276/SX1278 modules (2x - transmitter & receiver)
- ✅ Raspberry Pi (3/4/Zero W)
- ✅ Pressure sensor (analog output)
- ✅ Moisture sensor (capacitive/resistive)
- ✅ Acoustic sensor (microphone module)
- ✅ Breadboard and jumper wires
- ✅ Power supplies

### Software
- ✅ PlatformIO or Arduino IDE
- ✅ Python 3.8+
- ✅ PostgreSQL 12+
- ✅ Modern web browser

---

## 🔧 Part 1: ESP32 Transmitter Setup

### 1.1 Hardware Connections

**LoRa Module to ESP32:**
```
LoRa VCC  → ESP32 3.3V
LoRa GND  → ESP32 GND
LoRa SCK  → ESP32 GPIO 5
LoRa MISO → ESP32 GPIO 19
LoRa MOSI → ESP32 GPIO 27
LoRa NSS  → ESP32 GPIO 18
LoRa RST  → ESP32 GPIO 14
LoRa DIO0 → ESP32 GPIO 26
```

**Sensors to ESP32:**
```
Pressure Sensor → ESP32 GPIO 34 (ADC)
Moisture Sensor → ESP32 GPIO 35 (ADC)
Acoustic Sensor → ESP32 GPIO 32 (ADC)
```

### 1.2 Software Installation

#### Option A: Using PlatformIO (Recommended)
```bash
# Install PlatformIO
pip install platformio

# Navigate to project
cd esp32_transmitter

# Build and upload
pio run --target upload

# Monitor serial output
pio device monitor
```

#### Option B: Using Arduino IDE
1. Install ESP32 board support:
   - File → Preferences → Additional Board URLs
   - Add: `https://dl.espressif.com/dl/package_esp32_index.json`
2. Install LoRa library:
   - Sketch → Include Library → Manage Libraries
   - Search and install "LoRa by Sandeep Mistry"
3. Open `esp32_transmitter/src/main.cpp`
4. Select board: "ESP32 Dev Module"
5. Upload code

### 1.3 Configuration

Edit `main.cpp` to adjust:
- **LoRa Frequency**: Change `LORA_FREQUENCY` (433E6, 868E6, or 915E6)
- **Transmission Interval**: Modify `TRANSMISSION_INTERVAL` (milliseconds)
- **Sensor Pins**: Update pin definitions if needed

### 1.4 Testing
- Open Serial Monitor (115200 baud)
- Verify sensor readings are displayed
- Check LoRa transmission confirmations

---

## 🍓 Part 2: Raspberry Pi Receiver Setup

### 2.1 Hardware Connections

**LoRa Module to Raspberry Pi:**
```
LoRa VCC  → RPi Pin 1  (3.3V)
LoRa GND  → RPi Pin 6  (GND)
LoRa SCK  → RPi Pin 23 (GPIO 11)
LoRa MISO → RPi Pin 21 (GPIO 9)
LoRa MOSI → RPi Pin 19 (GPIO 10)
LoRa NSS  → RPi Pin 24 (GPIO 8)
LoRa RST  → RPi Pin 22 (GPIO 25)
LoRa DIO0 → RPi Pin 7  (GPIO 4)
```

### 2.2 Raspberry Pi OS Setup

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Enable SPI
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable

# Reboot
sudo reboot
```

### 2.3 Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE leaksense;
CREATE USER leaksense_user WITH PASSWORD 'leaksense_pass';
GRANT ALL PRIVILEGES ON DATABASE leaksense TO leaksense_user;
\q
EOF

# Load database schema
sudo -u postgres psql leaksense < database/schema.sql
```

### 2.4 Install Python Dependencies

```bash
cd raspberry_pi_receiver

# Install system dependencies
sudo apt install python3-pip python3-dev -y

# Install Python packages
pip3 install -r requirements.txt
```

### 2.5 Test Database Connection

```bash
python3 database.py
```

### 2.6 Run LoRa Receiver

```bash
# Manual start
python3 lora_receiver.py

# Or create systemd service for auto-start
sudo nano /etc/systemd/system/leaksense-receiver.service
```

Paste this content:
```ini
[Unit]
Description=LeakSense LoRa Receiver
After=network.target postgresql.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Leaksense/raspberry_pi_receiver
ExecStart=/usr/bin/python3 lora_receiver.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable leaksense-receiver
sudo systemctl start leaksense-receiver
sudo systemctl status leaksense-receiver
```

---

## 🌐 Part 3: Flask Backend Setup

### 3.1 Install Dependencies

```bash
cd flask_backend
pip3 install -r requirements.txt
```

### 3.2 Configure Environment (Optional)

Create `.env` file:
```bash
nano .env
```

Add:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=leaksense
DB_USER=leaksense_user
DB_PASSWORD=leaksense_pass
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
```

### 3.3 Test Flask App

```bash
python3 app.py
```

Visit: `http://localhost:5000`

### 3.4 Production Deployment

Install Gunicorn:
```bash
pip3 install gunicorn
```

Create systemd service:
```bash
sudo nano /etc/systemd/system/leaksense-api.service
```

Paste:
```ini
[Unit]
Description=LeakSense Flask API
After=network.target postgresql.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Leaksense/flask_backend
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable leaksense-api
sudo systemctl start leaksense-api
sudo systemctl status leaksense-api
```

---

## 🎨 Part 4: Web Frontend

The web frontend is served automatically by Flask from the `web_frontend` directory.

### 4.1 Access Dashboard

Open browser and navigate to:
```
http://raspberry-pi-ip:5000
```

### 4.2 Features
- Real-time sensor gauges
- Interactive charts
- Alert notifications
- Statistics display

---

## 🧪 Testing the Complete System

### 1. Start ESP32 Transmitter
- Power on ESP32
- Verify sensor readings in serial monitor
- Confirm LoRa transmissions

### 2. Verify Raspberry Pi Reception
```bash
# Check receiver logs
sudo journalctl -u leaksense-receiver -f
```

### 3. Check Database
```bash
psql -U leaksense_user -d leaksense -h localhost
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;
\q
```

### 4. Test API
```bash
# Health check
curl http://localhost:5000/api/health

# Latest reading
curl http://localhost:5000/api/sensors/latest

# Statistics
curl http://localhost:5000/api/sensors/statistics?hours=24
```

### 5. Access Web Dashboard
Open browser: `http://raspberry-pi-ip:5000`

---

## 🔍 Troubleshooting

### ESP32 Issues

**LoRa initialization failed:**
- Check wiring connections
- Verify 3.3V power supply (not 5V!)
- Ensure correct LoRa frequency

**No sensor readings:**
- Verify sensor connections
- Check sensor power supply
- Test sensors individually

### Raspberry Pi Issues

**SPI not working:**
```bash
lsmod | grep spi
# Should show spi_bcm2835
```

**LoRa module not detected:**
- Double-check wiring
- Verify 3.3V power
- Check GPIO permissions

**Database connection failed:**
```bash
sudo systemctl status postgresql
psql -U leaksense_user -d leaksense -h localhost
```

### Web Dashboard Issues

**No data displayed:**
- Check API endpoint in browser console
- Verify Flask is running
- Check CORS settings

**Charts not rendering:**
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify data format

---

## 📊 Monitoring & Maintenance

### View Logs
```bash
# Receiver logs
sudo journalctl -u leaksense-receiver -f

# API logs
sudo journalctl -u leaksense-api -f
```

### Database Maintenance
```bash
# Cleanup old data (30+ days)
psql -U leaksense_user -d leaksense -h localhost
SELECT cleanup_old_data(30);

# Backup database
pg_dump -U leaksense_user leaksense > backup_$(date +%Y%m%d).sql
```

### System Health
```bash
# Check services
sudo systemctl status leaksense-receiver
sudo systemctl status leaksense-api
sudo systemctl status postgresql

# Check disk space
df -h

# Check memory
free -h
```

---

## 🚀 Next Steps

1. **Customize Thresholds**: Adjust alert thresholds in web frontend
2. **Add More Sensors**: Extend ESP32 code for additional sensors
3. **Email Alerts**: Implement email notifications for critical alerts
4. **Mobile App**: Create mobile app using API
5. **Data Analytics**: Add ML models for anomaly detection
6. **Remote Access**: Set up VPN or reverse proxy for remote access

---

## 📚 Additional Resources

- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [LoRa Library](https://github.com/sandeepmistry/arduino-LoRa)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

---

## 💡 Tips

- Use quality jumper wires to avoid connection issues
- Keep LoRa antennas away from metal objects
- Monitor system temperature on Raspberry Pi
- Regular database backups are essential
- Use UPS for continuous operation
- Document any custom modifications

---

## 🆘 Support

For issues or questions:
1. Check troubleshooting section
2. Review component README files
3. Check system logs
4. Verify hardware connections

---

**Happy Monitoring! 🎉**
