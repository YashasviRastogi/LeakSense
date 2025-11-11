# LeakSense Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Checklist
- [ ] ESP32 with LoRa module assembled
- [ ] Raspberry Pi with LoRa module connected
- [ ] PostgreSQL installed
- [ ] Python 3.8+ installed

---

## Step 1: Database Setup (2 minutes)

```bash
# Create database
sudo -u postgres psql << EOF
CREATE DATABASE leaksense;
CREATE USER leaksense_user WITH PASSWORD 'leaksense_pass';
GRANT ALL PRIVILEGES ON DATABASE leaksense TO leaksense_user;
\q
EOF

# Load schema
cd Leaksense/database
sudo -u postgres psql leaksense < schema.sql
```

---

## Step 2: ESP32 Transmitter (1 minute)

```bash
cd Leaksense/esp32_transmitter

# Using PlatformIO
pio run --target upload

# Or use Arduino IDE to upload main.cpp
```

---

## Step 3: Raspberry Pi Receiver (1 minute)

```bash
cd Leaksense/raspberry_pi_receiver

# Install dependencies
pip3 install -r requirements.txt

# Start receiver
python3 lora_receiver.py
```

---

## Step 4: Flask Backend (1 minute)

```bash
# Open new terminal
cd Leaksense/flask_backend

# Install dependencies
pip3 install -r requirements.txt

# Start server
python3 app.py
```

---

## Step 5: Access Dashboard

Open browser: **http://localhost:5000**

---

## 🎉 You're Done!

You should now see:
- ✅ Real-time sensor data on dashboard
- ✅ Animated gauges updating
- ✅ Live charts displaying trends
- ✅ Connection status showing "Connected"

---

## 🔍 Verify Everything Works

### Check ESP32
```
Serial Monitor should show:
- Sensor readings
- LoRa transmission confirmations
- Packet numbers incrementing
```

### Check Raspberry Pi
```bash
# Should show received packets
sudo journalctl -u leaksense-receiver -f
```

### Check Database
```bash
psql -U leaksense_user -d leaksense -h localhost
SELECT COUNT(*) FROM sensor_readings;
\q
```

### Check API
```bash
curl http://localhost:5000/api/sensors/latest
```

---

## ⚠️ Common Issues

### "LoRa initialization failed"
- Check wiring (especially 3.3V, not 5V!)
- Verify SPI is enabled on Raspberry Pi

### "Database connection failed"
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in config files

### "No data on dashboard"
- Verify Flask is running
- Check browser console for errors
- Ensure ESP32 is transmitting

---

## 📚 Next Steps

1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
2. Check [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for wiring diagrams
3. Customize thresholds in `web_frontend/js/app.js`
4. Set up systemd services for auto-start

---

## 🆘 Need Help?

- Check logs: `sudo journalctl -u leaksense-receiver -f`
- Test database: `python3 database.py`
- Verify API: `curl http://localhost:5000/api/health`
- Review troubleshooting section in SETUP_GUIDE.md

---

**Happy Monitoring! 🎊**
