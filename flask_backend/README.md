# Flask Backend API

## Overview
REST API server for LeakSense sensor data visualization.

## Installation

### 1. Install Dependencies
```bash
cd flask_backend
pip3 install -r requirements.txt
```

### 2. Configure Environment (Optional)
Create `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=leaksense
DB_USER=leaksense_user
DB_PASSWORD=leaksense_pass
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 3. Run Server
```bash
python3 app.py
```

Server will start at: `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server and database status.

### Latest Reading
```
GET /api/sensors/latest
```
Returns the most recent sensor reading.

**Response:**
```json
{
  "id": 123,
  "pressure": 45.67,
  "moisture": 32.45,
  "acoustic": 55.30,
  "rssi": -85,
  "snr": 8.5,
  "timestamp": "2024-01-15T10:30:00",
  "created_at": "2024-01-15T10:30:00"
}
```

### Recent Readings
```
GET /api/sensors/recent?limit=50
```
Returns recent sensor readings.

**Parameters:**
- `limit` (optional): Number of records (default: 50, max: 1000)

### Time Range Readings
```
GET /api/sensors/range?hours=24
```
Returns readings within specified time range.

**Parameters:**
- `hours` (optional): Time range in hours (default: 24, max: 168)

### Statistics
```
GET /api/sensors/statistics?hours=24
```
Returns statistical summary of sensor data.

**Response:**
```json
{
  "total_readings": 1440,
  "avg_pressure": 45.67,
  "min_pressure": 40.12,
  "max_pressure": 52.34,
  "std_pressure": 3.45,
  "avg_moisture": 32.45,
  "avg_acoustic": 55.30,
  "period_hours": 24
}
```

### Alerts
```
GET /api/sensors/alerts?hours=24
```
Returns readings that exceed threshold values.

**Thresholds:**
- Moisture > 70%
- Acoustic > 75 dB
- Pressure < 20 PSI or > 80 PSI

### Chart Data
```
GET /api/sensors/chart-data?hours=1
```
Returns formatted data for Chart.js visualization.

## Running as Service

### systemd Service
Create `/etc/systemd/system/leaksense-api.service`:
```ini
[Unit]
Description=LeakSense Flask API
After=network.target postgresql.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Leaksense/flask_backend
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 /home/pi/Leaksense/flask_backend/app.py
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

## Testing API

### Using curl
```bash
# Health check
curl http://localhost:5000/api/health

# Latest reading
curl http://localhost:5000/api/sensors/latest

# Recent readings
curl http://localhost:5000/api/sensors/recent?limit=10

# Statistics
curl http://localhost:5000/api/sensors/statistics?hours=24
```

### Using Python
```python
import requests

response = requests.get('http://localhost:5000/api/sensors/latest')
data = response.json()
print(data)
```

## CORS Configuration
By default, CORS is enabled for all origins. To restrict:
```python
# In config.py
CORS_ORIGINS = 'http://localhost:3000,https://yourdomain.com'
```

## Production Deployment
For production, use a WSGI server like Gunicorn:

```bash
pip3 install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
