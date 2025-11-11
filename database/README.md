# LeakSense Database

## Overview
PostgreSQL database schema for storing sensor readings and providing efficient queries.

## Database Structure

### Main Table: sensor_readings
Stores all sensor data with timestamps.

**Columns:**
- `id` - Auto-incrementing primary key
- `pressure` - Pressure reading (PSI)
- `moisture` - Moisture level (%)
- `acoustic` - Acoustic level (dB)
- `rssi` - Signal strength (dBm)
- `snr` - Signal-to-noise ratio (dB)
- `timestamp` - Reading timestamp
- `created_at` - Record creation timestamp

### Views

#### recent_readings
Last 100 sensor readings for quick access.

#### hourly_averages
Aggregated hourly statistics for trend analysis.

#### daily_statistics
Daily aggregated data with standard deviations.

#### alert_readings
Readings that exceed threshold values.

### Functions

#### cleanup_old_data(days_to_keep)
Removes sensor readings older than specified days.

```sql
SELECT cleanup_old_data(30); -- Delete data older than 30 days
```

#### get_sensor_stats(hours_back)
Returns statistical summary for specified time period.

```sql
SELECT * FROM get_sensor_stats(24); -- Last 24 hours stats
```

## Setup Instructions

### 1. Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database and User
```bash
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE leaksense;
CREATE USER leaksense_user WITH PASSWORD 'leaksense_pass';
GRANT ALL PRIVILEGES ON DATABASE leaksense TO leaksense_user;
\q
```

### 3. Run Schema Script
```bash
sudo -u postgres psql leaksense < schema.sql
```

### 4. Verify Installation
```bash
psql -U leaksense_user -d leaksense -h localhost

# In PostgreSQL prompt:
\dt                              # List tables
\d sensor_readings              # Describe table
SELECT * FROM sensor_readings;  # View data
\q
```

## Configuration

### Connection String
```
postgresql://leaksense_user:leaksense_pass@localhost:5432/leaksense
```

### Environment Variables
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=leaksense
export DB_USER=leaksense_user
export DB_PASSWORD=leaksense_pass
```

## Maintenance

### Backup Database
```bash
pg_dump -U leaksense_user leaksense > leaksense_backup.sql
```

### Restore Database
```bash
psql -U leaksense_user leaksense < leaksense_backup.sql
```

### Cleanup Old Data
```sql
-- Delete data older than 30 days
SELECT cleanup_old_data(30);

-- Or manually
DELETE FROM sensor_readings WHERE timestamp < NOW() - INTERVAL '30 days';
```

### Optimize Database
```sql
-- Vacuum and analyze
VACUUM ANALYZE sensor_readings;

-- Reindex
REINDEX TABLE sensor_readings;
```

## Queries

### Latest Reading
```sql
SELECT * FROM sensor_readings
ORDER BY timestamp DESC
LIMIT 1;
```

### Readings in Last Hour
```sql
SELECT * FROM sensor_readings
WHERE timestamp >= NOW() - INTERVAL '1 hour'
ORDER BY timestamp ASC;
```

### Statistics for Last 24 Hours
```sql
SELECT 
    COUNT(*) as total,
    AVG(pressure) as avg_pressure,
    AVG(moisture) as avg_moisture,
    AVG(acoustic) as avg_acoustic
FROM sensor_readings
WHERE timestamp >= NOW() - INTERVAL '24 hours';
```

### Alert Readings
```sql
SELECT * FROM alert_readings
WHERE timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;
```

### Hourly Trends
```sql
SELECT * FROM hourly_averages
WHERE hour >= NOW() - INTERVAL '7 days'
ORDER BY hour ASC;
```

## Performance Tips

1. **Indexes**: Already created on timestamp and sensor columns
2. **Partitioning**: Consider partitioning by date for large datasets
3. **Archiving**: Move old data to archive tables
4. **Connection Pooling**: Use pgBouncer for high-traffic scenarios

## Security

### Change Default Password
```sql
ALTER USER leaksense_user WITH PASSWORD 'new_secure_password';
```

### Restrict Access
Edit `/etc/postgresql/*/main/pg_hba.conf`:
```
# Allow only local connections
local   leaksense   leaksense_user   md5
host    leaksense   leaksense_user   127.0.0.1/32   md5
```

### Enable SSL
```sql
ALTER SYSTEM SET ssl = on;
SELECT pg_reload_conf();
```

## Monitoring

### Check Database Size
```sql
SELECT pg_size_pretty(pg_database_size('leaksense'));
```

### Check Table Size
```sql
SELECT pg_size_pretty(pg_total_relation_size('sensor_readings'));
```

### Active Connections
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'leaksense';
```

### Query Performance
```sql
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```
