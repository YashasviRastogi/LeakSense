# LeakSense API Documentation

## 📡 REST API Reference

**Base URL**: `http://your-server:5000/api`

**Content-Type**: `application/json`

---

## 🔍 Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/sensors/latest` | GET | Latest sensor reading |
| `/api/sensors/recent` | GET | Recent readings |
| `/api/sensors/range` | GET | Time range query |
| `/api/sensors/statistics` | GET | Statistical summary |
| `/api/sensors/alerts` | GET | Alert readings |
| `/api/sensors/chart-data` | GET | Chart-ready data |

---

## 📋 Detailed Endpoints

### 1. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check API and database connectivity

**Parameters**: None

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Status Codes**:
- `200 OK` - System healthy
- `503 Service Unavailable` - Database disconnected

**Example**:
```bash
curl http://localhost:5000/api/health
```

---

### 2. Latest Sensor Reading

**Endpoint**: `GET /api/sensors/latest`

**Description**: Get the most recent sensor reading

**Parameters**: None

**Response**:
```json
{
  "id": 12345,
  "pressure": 45.67,
  "moisture": 32.45,
  "acoustic": 55.30,
  "rssi": -85,
  "snr": 8.5,
  "timestamp": "2024-01-15T10:30:00",
  "created_at": "2024-01-15T10:30:00"
}
```

**Status Codes**:
- `200 OK` - Reading found
- `404 Not Found` - No data available
- `500 Internal Server Error` - Database error

**Example**:
```bash
curl http://localhost:5000/api/sensors/latest
```

**JavaScript**:
```javascript
fetch('http://localhost:5000/api/sensors/latest')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

### 3. Recent Readings

**Endpoint**: `GET /api/sensors/recent`

**Description**: Get recent sensor readings

**Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `limit` | integer | 50 | 1000 | Number of records |

**Response**:
```json
{
  "count": 50,
  "data": [
    {
      "id": 12345,
      "pressure": 45.67,
      "moisture": 32.45,
      "acoustic": 55.30,
      "rssi": -85,
      "snr": 8.5,
      "timestamp": "2024-01-15T10:30:00",
      "created_at": "2024-01-15T10:30:00"
    },
    // ... more readings
  ]
}
```

**Status Codes**:
- `200 OK` - Success
- `500 Internal Server Error` - Database error

**Examples**:
```bash
# Get last 10 readings
curl http://localhost:5000/api/sensors/recent?limit=10

# Get last 100 readings
curl http://localhost:5000/api/sensors/recent?limit=100
```

**JavaScript**:
```javascript
fetch('http://localhost:5000/api/sensors/recent?limit=20')
  .then(response => response.json())
  .then(data => {
    console.log(`Retrieved ${data.count} readings`);
    data.data.forEach(reading => {
      console.log(`Pressure: ${reading.pressure} PSI`);
    });
  });
```

---

### 4. Time Range Query

**Endpoint**: `GET /api/sensors/range`

**Description**: Get readings within a time range

**Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `hours` | integer | 24 | 168 | Hours back from now |

**Response**:
```json
{
  "count": 288,
  "start_time": "2024-01-14T10:30:00",
  "end_time": "2024-01-15T10:30:00",
  "data": [
    {
      "id": 12345,
      "pressure": 45.67,
      "moisture": 32.45,
      "acoustic": 55.30,
      "rssi": -85,
      "snr": 8.5,
      "timestamp": "2024-01-15T10:30:00",
      "created_at": "2024-01-15T10:30:00"
    },
    // ... more readings
  ]
}
```

**Status Codes**:
- `200 OK` - Success
- `500 Internal Server Error` - Database error

**Examples**:
```bash
# Last 1 hour
curl http://localhost:5000/api/sensors/range?hours=1

# Last 24 hours
curl http://localhost:5000/api/sensors/range?hours=24

# Last 7 days
curl http://localhost:5000/api/sensors/range?hours=168
```

**Python**:
```python
import requests

response = requests.get('http://localhost:5000/api/sensors/range?hours=6')
data = response.json()
print(f"Retrieved {data['count']} readings from last 6 hours")
```

---

### 5. Statistics

**Endpoint**: `GET /api/sensors/statistics`

**Description**: Get statistical summary of sensor data

**Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `hours` | integer | 24 | 168 | Hours back from now |

**Response**:
```json
{
  "total_readings": 1440,
  "avg_pressure": 45.67,
  "min_pressure": 40.12,
  "max_pressure": 52.34,
  "std_pressure": 3.45,
  "avg_moisture": 32.45,
  "min_moisture": 28.10,
  "max_moisture": 38.90,
  "std_moisture": 2.87,
  "avg_acoustic": 55.30,
  "min_acoustic": 50.20,
  "max_acoustic": 62.40,
  "std_acoustic": 4.12,
  "avg_rssi": -85.5,
  "min_rssi": -95,
  "max_rssi": -75,
  "period_hours": 24,
  "start_time": "2024-01-14T10:30:00",
  "end_time": "2024-01-15T10:30:00"
}
```

**Status Codes**:
- `200 OK` - Success
- `404 Not Found` - No data in range
- `500 Internal Server Error` - Database error

**Examples**:
```bash
# Last 24 hours stats
curl http://localhost:5000/api/sensors/statistics?hours=24

# Last week stats
curl http://localhost:5000/api/sensors/statistics?hours=168
```

**JavaScript**:
```javascript
fetch('http://localhost:5000/api/sensors/statistics?hours=24')
  .then(response => response.json())
  .then(stats => {
    console.log(`Average Pressure: ${stats.avg_pressure.toFixed(2)} PSI`);
    console.log(`Average Moisture: ${stats.avg_moisture.toFixed(2)} %`);
    console.log(`Total Readings: ${stats.total_readings}`);
  });
```

---

### 6. Alerts

**Endpoint**: `GET /api/sensors/alerts`

**Description**: Get readings that exceed threshold values

**Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `hours` | integer | 24 | 168 | Hours back from now |

**Thresholds**:
- Moisture > 70%
- Acoustic > 75 dB
- Pressure < 20 PSI or > 80 PSI

**Response**:
```json
{
  "count": 5,
  "thresholds": {
    "moisture_max": 70,
    "acoustic_max": 75,
    "pressure_min": 20,
    "pressure_max": 80
  },
  "data": [
    {
      "id": 12345,
      "pressure": 45.67,
      "moisture": 75.30,
      "acoustic": 55.30,
      "rssi": -85,
      "snr": 8.5,
      "timestamp": "2024-01-15T10:30:00",
      "created_at": "2024-01-15T10:30:00",
      "alert_types": ["high_moisture"]
    },
    {
      "id": 12346,
      "pressure": 85.20,
      "moisture": 32.45,
      "acoustic": 78.50,
      "rssi": -83,
      "snr": 9.1,
      "timestamp": "2024-01-15T10:25:00",
      "created_at": "2024-01-15T10:25:00",
      "alert_types": ["high_pressure", "high_acoustic"]
    }
  ]
}
```

**Alert Types**:
- `high_moisture` - Moisture > 70%
- `high_acoustic` - Acoustic > 75 dB
- `low_pressure` - Pressure < 20 PSI
- `high_pressure` - Pressure > 80 PSI

**Status Codes**:
- `200 OK` - Success (may return 0 alerts)
- `500 Internal Server Error` - Database error

**Examples**:
```bash
# Last 24 hours alerts
curl http://localhost:5000/api/sensors/alerts?hours=24

# Last hour alerts
curl http://localhost:5000/api/sensors/alerts?hours=1
```

**Python**:
```python
import requests

response = requests.get('http://localhost:5000/api/sensors/alerts?hours=24')
data = response.json()

if data['count'] > 0:
    print(f"⚠️  {data['count']} alerts in last 24 hours!")
    for alert in data['data']:
        print(f"  - {', '.join(alert['alert_types'])} at {alert['timestamp']}")
else:
    print("✅ No alerts in last 24 hours")
```

---

### 7. Chart Data

**Endpoint**: `GET /api/sensors/chart-data`

**Description**: Get formatted data for Chart.js visualization

**Parameters**:
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `hours` | integer | 1 | 24 | Hours back from now |

**Response**:
```json
{
  "labels": [
    "10:30:00",
    "10:35:00",
    "10:40:00",
    // ... more timestamps
  ],
  "pressure": [45.67, 46.12, 45.89, ...],
  "moisture": [32.45, 33.10, 32.78, ...],
  "acoustic": [55.30, 56.20, 55.45, ...]
}
```

**Status Codes**:
- `200 OK` - Success
- `500 Internal Server Error` - Database error

**Examples**:
```bash
# Last hour for chart
curl http://localhost:5000/api/sensors/chart-data?hours=1

# Last 6 hours for chart
curl http://localhost:5000/api/sensors/chart-data?hours=6
```

**JavaScript with Chart.js**:
```javascript
fetch('http://localhost:5000/api/sensors/chart-data?hours=1')
  .then(response => response.json())
  .then(data => {
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Pressure (PSI)',
            data: data.pressure,
            borderColor: 'rgb(59, 130, 246)'
          },
          {
            label: 'Moisture (%)',
            data: data.moisture,
            borderColor: 'rgb(6, 182, 212)'
          },
          {
            label: 'Acoustic (dB)',
            data: data.acoustic,
            borderColor: 'rgb(139, 92, 246)'
          }
        ]
      }
    });
  });
```

---

## 🔐 Authentication (Future)

Currently, the API is open. For production, implement authentication:

### JWT Authentication
```javascript
// Login
fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'user',
    password: 'pass'
  })
})
.then(response => response.json())
.then(data => {
  const token = data.token;
  
  // Use token in requests
  fetch('http://localhost:5000/api/sensors/latest', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
});
```

---

## 🚨 Error Responses

### Standard Error Format
```json
{
  "error": "Error message description"
}
```

### Common Errors

**400 Bad Request**:
```json
{
  "error": "Invalid parameter value"
}
```

**404 Not Found**:
```json
{
  "error": "Endpoint not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Database connection failed"
}
```

**503 Service Unavailable**:
```json
{
  "error": "Service temporarily unavailable"
}
```

---

## 📊 Rate Limiting (Future)

Implement rate limiting for production:

```
Rate Limit: 100 requests per minute
Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1642248000
```

---

## 🔄 WebSocket Support (Future)

For real-time updates:

```javascript
const socket = new WebSocket('ws://localhost:5000/ws');

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New sensor reading:', data);
};
```

---

## 📝 Code Examples

### Python Client
```python
import requests
import time

class LeakSenseClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def get_latest(self):
        response = requests.get(f'{self.base_url}/api/sensors/latest')
        return response.json()
    
    def get_statistics(self, hours=24):
        response = requests.get(
            f'{self.base_url}/api/sensors/statistics',
            params={'hours': hours}
        )
        return response.json()
    
    def monitor_alerts(self, interval=60):
        while True:
            alerts = requests.get(
                f'{self.base_url}/api/sensors/alerts',
                params={'hours': 1}
            ).json()
            
            if alerts['count'] > 0:
                print(f"⚠️  {alerts['count']} new alerts!")
            
            time.sleep(interval)

# Usage
client = LeakSenseClient()
latest = client.get_latest()
print(f"Pressure: {latest['pressure']} PSI")
```

### JavaScript Client
```javascript
class LeakSenseAPI {
  constructor(baseUrl = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }
  
  async getLatest() {
    const response = await fetch(`${this.baseUrl}/api/sensors/latest`);
    return await response.json();
  }
  
  async getStatistics(hours = 24) {
    const response = await fetch(
      `${this.baseUrl}/api/sensors/statistics?hours=${hours}`
    );
    return await response.json();
  }
  
  async getChartData(hours = 1) {
    const response = await fetch(
      `${this.baseUrl}/api/sensors/chart-data?hours=${hours}`
    );
    return await response.json();
  }
}

// Usage
const api = new LeakSenseAPI();

api.getLatest().then(data => {
  console.log(`Pressure: ${data.pressure} PSI`);
  console.log(`Moisture: ${data.moisture} %`);
});
```

### cURL Examples
```bash
# Health check
curl -X GET http://localhost:5000/api/health

# Latest reading
curl -X GET http://localhost:5000/api/sensors/latest

# Recent readings (last 10)
curl -X GET "http://localhost:5000/api/sensors/recent?limit=10"

# Statistics (last 24 hours)
curl -X GET "http://localhost:5000/api/sensors/statistics?hours=24"

# Alerts (last hour)
curl -X GET "http://localhost:5000/api/sensors/alerts?hours=1"

# Chart data (last 6 hours)
curl -X GET "http://localhost:5000/api/sensors/chart-data?hours=6"

# Pretty print JSON
curl -X GET http://localhost:5000/api/sensors/latest | python -m json.tool
```

---

## 🧪 Testing

### Postman Collection
Import this collection for testing:

```json
{
  "info": {
    "name": "LeakSense API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/health"
      }
    },
    {
      "name": "Latest Reading",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/sensors/latest"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000"
    }
  ]
}
```

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [JSON API Specification](https://jsonapi.org/)

---

**Happy API Integration! 🚀**
