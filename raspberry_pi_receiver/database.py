#!/usr/bin/env python3
"""
Database module for LeakSense
Handles PostgreSQL connections and data storage
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import os

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'leaksense'),
    'user': os.getenv('DB_USER', 'leaksense_user'),
    'password': os.getenv('DB_PASSWORD', 'leaksense_pass')
}


class Database:
    """Database handler for sensor data"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print(f"✅ Connected to PostgreSQL database: {DB_CONFIG['database']}")
        except psycopg2.Error as e:
            print(f"❌ Database connection error: {e}")
            raise
    
    def create_tables(self):
        """Create necessary database tables"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id SERIAL PRIMARY KEY,
            pressure REAL NOT NULL,
            moisture REAL NOT NULL,
            acoustic REAL NOT NULL,
            rssi INTEGER,
            snr REAL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_timestamp ON sensor_readings(timestamp DESC);
        CREATE INDEX IF NOT EXISTS idx_created_at ON sensor_readings(created_at DESC);
        """
        
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("✅ Database tables verified/created")
        except psycopg2.Error as e:
            print(f"❌ Error creating tables: {e}")
            self.conn.rollback()
            raise
    
    def insert_sensor_data(self, pressure, moisture, acoustic, rssi=None, snr=None, timestamp=None):
        """Insert sensor reading into database"""
        if timestamp is None:
            timestamp = datetime.now()
        
        insert_query = """
        INSERT INTO sensor_readings (pressure, moisture, acoustic, rssi, snr, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        try:
            self.cursor.execute(insert_query, (pressure, moisture, acoustic, rssi, snr, timestamp))
            self.conn.commit()
            record_id = self.cursor.fetchone()['id']
            return record_id
        except psycopg2.Error as e:
            print(f"❌ Error inserting data: {e}")
            self.conn.rollback()
            raise
    
    def get_latest_readings(self, limit=10):
        """Get latest sensor readings"""
        query = """
        SELECT * FROM sensor_readings
        ORDER BY timestamp DESC
        LIMIT %s;
        """
        
        try:
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"❌ Error fetching data: {e}")
            return []
    
    def get_readings_by_timerange(self, start_time, end_time=None):
        """Get sensor readings within a time range"""
        if end_time is None:
            end_time = datetime.now()
        
        query = """
        SELECT * FROM sensor_readings
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC;
        """
        
        try:
            self.cursor.execute(query, (start_time, end_time))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"❌ Error fetching data: {e}")
            return []
    
    def get_statistics(self, hours=24):
        """Get statistical summary of sensor data"""
        start_time = datetime.now() - timedelta(hours=hours)
        
        query = """
        SELECT 
            COUNT(*) as total_readings,
            AVG(pressure) as avg_pressure,
            MIN(pressure) as min_pressure,
            MAX(pressure) as max_pressure,
            AVG(moisture) as avg_moisture,
            MIN(moisture) as min_moisture,
            MAX(moisture) as max_moisture,
            AVG(acoustic) as avg_acoustic,
            MIN(acoustic) as min_acoustic,
            MAX(acoustic) as max_acoustic,
            AVG(rssi) as avg_rssi
        FROM sensor_readings
        WHERE timestamp >= %s;
        """
        
        try:
            self.cursor.execute(query, (start_time,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            print(f"❌ Error fetching statistics: {e}")
            return None
    
    def cleanup_old_data(self, days=30):
        """Delete sensor readings older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        delete_query = """
        DELETE FROM sensor_readings
        WHERE timestamp < %s;
        """
        
        try:
            self.cursor.execute(delete_query, (cutoff_date,))
            deleted_count = self.cursor.rowcount
            self.conn.commit()
            print(f"✅ Deleted {deleted_count} old records")
            return deleted_count
        except psycopg2.Error as e:
            print(f"❌ Error deleting old data: {e}")
            self.conn.rollback()
            return 0
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ Database connection closed")


# Test database connection
if __name__ == "__main__":
    print("Testing database connection...\n")
    
    db = Database()
    try:
        db.connect()
        db.create_tables()
        
        # Test insert
        print("\nTesting data insertion...")
        record_id = db.insert_sensor_data(
            pressure=45.5,
            moisture=32.1,
            acoustic=55.8,
            rssi=-85,
            snr=8.5
        )
        print(f"✅ Inserted record ID: {record_id}")
        
        # Test retrieval
        print("\nTesting data retrieval...")
        latest = db.get_latest_readings(limit=5)
        print(f"✅ Retrieved {len(latest)} records")
        
        for record in latest:
            print(f"  ID: {record['id']}, Pressure: {record['pressure']}, "
                  f"Moisture: {record['moisture']}, Acoustic: {record['acoustic']}")
        
        # Test statistics
        print("\nTesting statistics...")
        stats = db.get_statistics(hours=24)
        if stats:
            print(f"✅ Total readings (24h): {stats['total_readings']}")
            print(f"  Avg Pressure: {stats['avg_pressure']:.2f} PSI")
            print(f"  Avg Moisture: {stats['avg_moisture']:.2f} %")
            print(f"  Avg Acoustic: {stats['avg_acoustic']:.2f} dB")
        
        db.close()
        print("\n✅ All database tests passed!")
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
