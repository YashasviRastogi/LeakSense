-- LeakSense Database Schema
-- PostgreSQL Database Setup

-- Create database (run as postgres user)
-- CREATE DATABASE leaksense;
-- CREATE USER leaksense_user WITH PASSWORD 'leaksense_pass';
-- GRANT ALL PRIVILEGES ON DATABASE leaksense TO leaksense_user;

-- Connect to leaksense database
\c leaksense

-- Create sensor_readings table
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    pressure REAL NOT NULL CHECK (pressure >= 0 AND pressure <= 200),
    moisture REAL NOT NULL CHECK (moisture >= 0 AND moisture <= 100),
    acoustic REAL NOT NULL CHECK (acoustic >= 0 AND acoustic <= 150),
    rssi INTEGER CHECK (rssi >= -120 AND rssi <= 0),
    snr REAL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_created_at ON sensor_readings(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pressure ON sensor_readings(pressure);
CREATE INDEX IF NOT EXISTS idx_moisture ON sensor_readings(moisture);
CREATE INDEX IF NOT EXISTS idx_acoustic ON sensor_readings(acoustic);

-- Create composite index for time-range queries
CREATE INDEX IF NOT EXISTS idx_timestamp_sensors ON sensor_readings(timestamp, pressure, moisture, acoustic);

-- Create view for recent readings
CREATE OR REPLACE VIEW recent_readings AS
SELECT * FROM sensor_readings
ORDER BY timestamp DESC
LIMIT 100;

-- Create view for hourly averages
CREATE OR REPLACE VIEW hourly_averages AS
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(pressure) as avg_pressure,
    AVG(moisture) as avg_moisture,
    AVG(acoustic) as avg_acoustic,
    MIN(pressure) as min_pressure,
    MAX(pressure) as max_pressure,
    MIN(moisture) as min_moisture,
    MAX(moisture) as max_moisture,
    MIN(acoustic) as min_acoustic,
    MAX(acoustic) as max_acoustic,
    COUNT(*) as reading_count
FROM sensor_readings
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour DESC;

-- Create view for daily statistics
CREATE OR REPLACE VIEW daily_statistics AS
SELECT 
    DATE_TRUNC('day', timestamp) as day,
    AVG(pressure) as avg_pressure,
    AVG(moisture) as avg_moisture,
    AVG(acoustic) as avg_acoustic,
    STDDEV(pressure) as std_pressure,
    STDDEV(moisture) as std_moisture,
    STDDEV(acoustic) as std_acoustic,
    MIN(pressure) as min_pressure,
    MAX(pressure) as max_pressure,
    MIN(moisture) as min_moisture,
    MAX(moisture) as max_moisture,
    MIN(acoustic) as min_acoustic,
    MAX(acoustic) as max_acoustic,
    COUNT(*) as reading_count
FROM sensor_readings
GROUP BY DATE_TRUNC('day', timestamp)
ORDER BY day DESC;

-- Create view for alerts (readings exceeding thresholds)
CREATE OR REPLACE VIEW alert_readings AS
SELECT 
    id,
    pressure,
    moisture,
    acoustic,
    timestamp,
    CASE 
        WHEN moisture > 70 THEN 'High Moisture'
        WHEN acoustic > 75 THEN 'High Acoustic'
        WHEN pressure < 20 THEN 'Low Pressure'
        WHEN pressure > 80 THEN 'High Pressure'
    END as alert_type
FROM sensor_readings
WHERE 
    moisture > 70 OR
    acoustic > 75 OR
    pressure < 20 OR
    pressure > 80
ORDER BY timestamp DESC;

-- Function to cleanup old data (older than 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_data(days_to_keep INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM sensor_readings
    WHERE timestamp < NOW() - INTERVAL '1 day' * days_to_keep;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get sensor statistics for a time period
CREATE OR REPLACE FUNCTION get_sensor_stats(hours_back INTEGER DEFAULT 24)
RETURNS TABLE (
    total_readings BIGINT,
    avg_pressure NUMERIC,
    min_pressure NUMERIC,
    max_pressure NUMERIC,
    avg_moisture NUMERIC,
    min_moisture NUMERIC,
    max_moisture NUMERIC,
    avg_acoustic NUMERIC,
    min_acoustic NUMERIC,
    max_acoustic NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT,
        ROUND(AVG(sr.pressure)::NUMERIC, 2),
        ROUND(MIN(sr.pressure)::NUMERIC, 2),
        ROUND(MAX(sr.pressure)::NUMERIC, 2),
        ROUND(AVG(sr.moisture)::NUMERIC, 2),
        ROUND(MIN(sr.moisture)::NUMERIC, 2),
        ROUND(MAX(sr.moisture)::NUMERIC, 2),
        ROUND(AVG(sr.acoustic)::NUMERIC, 2),
        ROUND(MIN(sr.acoustic)::NUMERIC, 2),
        ROUND(MAX(sr.acoustic)::NUMERIC, 2)
    FROM sensor_readings sr
    WHERE sr.timestamp >= NOW() - INTERVAL '1 hour' * hours_back;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update created_at
CREATE OR REPLACE FUNCTION update_created_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.created_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_created_at
BEFORE INSERT ON sensor_readings
FOR EACH ROW
EXECUTE FUNCTION update_created_at();

-- Grant permissions to leaksense_user
GRANT ALL PRIVILEGES ON TABLE sensor_readings TO leaksense_user;
GRANT USAGE, SELECT ON SEQUENCE sensor_readings_id_seq TO leaksense_user;
GRANT SELECT ON recent_readings TO leaksense_user;
GRANT SELECT ON hourly_averages TO leaksense_user;
GRANT SELECT ON daily_statistics TO leaksense_user;
GRANT SELECT ON alert_readings TO leaksense_user;

-- Insert sample data for testing (optional)
INSERT INTO sensor_readings (pressure, moisture, acoustic, rssi, snr, timestamp)
VALUES 
    (45.5, 32.1, 55.8, -85, 8.5, NOW() - INTERVAL '5 minutes'),
    (46.2, 33.5, 56.2, -83, 9.1, NOW() - INTERVAL '4 minutes'),
    (44.8, 31.8, 54.9, -87, 7.8, NOW() - INTERVAL '3 minutes'),
    (45.9, 32.7, 55.5, -84, 8.9, NOW() - INTERVAL '2 minutes'),
    (45.3, 32.3, 55.1, -86, 8.2, NOW() - INTERVAL '1 minute');

-- Display table info
\dt
\d sensor_readings

-- Display sample data
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 5;

-- Display statistics
SELECT * FROM get_sensor_stats(24);

COMMIT;
