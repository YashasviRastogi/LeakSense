# Raspberry Pi LoRa Receiver

## Hardware Requirements
- Raspberry Pi (3/4/Zero W)
- LoRa SX1276/SX1278 Module
- MicroSD card (16GB+)
- Power supply

## Pin Connections

### LoRa Module to Raspberry Pi
| LoRa Pin | RPi Pin | BCM GPIO |
|----------|---------|----------|
| VCC      | Pin 1   | 3.3V     |
| GND      | Pin 6   | GND      |
| SCK      | Pin 23  | GPIO 11  |
| MISO     | Pin 21  | GPIO 9   |
| MOSI     | Pin 19  | GPIO 10  |
| NSS/CS   | Pin 24  | GPIO 8   |
| RST      | Pin 22  | GPIO 25  |
| DIO0     | Pin 7   | GPIO 4   |

## Software Setup

### 1. Enable SPI
```bash
sudo raspi-config
# Interface Options -> SPI -> Enable
```

### 2. Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 3. Create Database
```bash
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE leaksense;
CREATE USER leaksense_user WITH PASSWORD 'leaksense_pass';
GRANT ALL PRIVILEGES ON DATABASE leaksense TO leaksense_user;
\q
```

### 4. Install Python Dependencies
```bash
cd raspberry_pi_receiver
pip3 install -r requirements.txt
```

### 5. Configure Environment Variables (Optional)
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=leaksense
export DB_USER=leaksense_user
export DB_PASSWORD=leaksense_pass
```

## Running the Receiver

### Manual Start
```bash
python3 lora_receiver.py
```

### Auto-start on Boot (systemd service)
Create `/etc/systemd/system/leaksense-receiver.service`:
```ini
[Unit]
Description=LeakSense LoRa Receiver
After=network.target postgresql.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Leaksense/raspberry_pi_receiver
ExecStart=/usr/bin/python3 /home/pi/Leaksense/raspberry_pi_receiver/lora_receiver.py
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

## Testing

### Test Database Connection
```bash
python3 database.py
```

### View Logs
```bash
# If running as service
sudo journalctl -u leaksense-receiver -f

# If running manually
# Output will appear in terminal
```

## Troubleshooting

### LoRa Module Not Detected
- Check SPI is enabled: `lsmod | grep spi`
- Verify wiring connections
- Check power supply (3.3V, not 5V!)

### Database Connection Failed
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials
- Test connection: `psql -U leaksense_user -d leaksense -h localhost`

### Permission Denied on GPIO
```bash
sudo usermod -a -G gpio,spi pi
# Logout and login again
```
