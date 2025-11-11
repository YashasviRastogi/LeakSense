#!/usr/bin/env python3
"""
LeakSense Flask Backend API
Provides REST API for sensor data visualization
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from config import Config

app = Flask(__name__, 
            static_folder='../web_frontend',
            template_folder='../web_frontend')
app.config.from_object(Config)
CORS(app)

# Database connection
def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None


@app.route('/')
def index():
    """Serve main dashboard page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    else:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'timestamp': datetime.now().isoformat()
        }), 503


@app.route('/api/sensors/latest', methods=['GET'])
def get_latest_reading():
    """Get the most recent sensor reading"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM sensor_readings
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        reading = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if reading:
            # Convert datetime to ISO format
            reading['timestamp'] = reading['timestamp'].isoformat()
            reading['created_at'] = reading['created_at'].isoformat()
            return jsonify(reading), 200
        else:
            return jsonify({'message': 'No data available'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/recent', methods=['GET'])
def get_recent_readings():
    """Get recent sensor readings"""
    limit = request.args.get('limit', default=50, type=int)
    limit = min(limit, 1000)  # Max 1000 records
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM sensor_readings
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert datetime objects to ISO format
        for reading in readings:
            reading['timestamp'] = reading['timestamp'].isoformat()
            reading['created_at'] = reading['created_at'].isoformat()
        
        return jsonify({
            'count': len(readings),
            'data': readings
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/range', methods=['GET'])
def get_readings_by_range():
    """Get sensor readings within a time range"""
    hours = request.args.get('hours', default=24, type=int)
    hours = min(hours, 168)  # Max 7 days
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM sensor_readings
            WHERE timestamp >= %s
            ORDER BY timestamp ASC
        """, (start_time,))
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert datetime objects to ISO format
        for reading in readings:
            reading['timestamp'] = reading['timestamp'].isoformat()
            reading['created_at'] = reading['created_at'].isoformat()
        
        return jsonify({
            'count': len(readings),
            'start_time': start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'data': readings
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/statistics', methods=['GET'])
def get_statistics():
    """Get statistical summary of sensor data"""
    hours = request.args.get('hours', default=24, type=int)
    hours = min(hours, 168)  # Max 7 days
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_readings,
                AVG(pressure) as avg_pressure,
                MIN(pressure) as min_pressure,
                MAX(pressure) as max_pressure,
                STDDEV(pressure) as std_pressure,
                AVG(moisture) as avg_moisture,
                MIN(moisture) as min_moisture,
                MAX(moisture) as max_moisture,
                STDDEV(moisture) as std_moisture,
                AVG(acoustic) as avg_acoustic,
                MIN(acoustic) as min_acoustic,
                MAX(acoustic) as max_acoustic,
                STDDEV(acoustic) as std_acoustic,
                AVG(rssi) as avg_rssi,
                MIN(rssi) as min_rssi,
                MAX(rssi) as max_rssi
            FROM sensor_readings
            WHERE timestamp >= %s
        """, (start_time,))
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if stats:
            # Convert Decimal to float
            stats = {k: float(v) if v is not None else None for k, v in stats.items()}
            stats['period_hours'] = hours
            stats['start_time'] = start_time.isoformat()
            stats['end_time'] = datetime.now().isoformat()
            return jsonify(stats), 200
        else:
            return jsonify({'message': 'No data available'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/alerts', methods=['GET'])
def get_alerts():
    """Get readings that exceed threshold values"""
    hours = request.args.get('hours', default=24, type=int)
    hours = min(hours, 168)
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    # Threshold values
    MOISTURE_THRESHOLD = 70.0
    ACOUSTIC_THRESHOLD = 75.0
    PRESSURE_MIN = 20.0
    PRESSURE_MAX = 80.0
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM sensor_readings
            WHERE timestamp >= %s
            AND (
                moisture > %s OR
                acoustic > %s OR
                pressure < %s OR
                pressure > %s
            )
            ORDER BY timestamp DESC
        """, (start_time, MOISTURE_THRESHOLD, ACOUSTIC_THRESHOLD, PRESSURE_MIN, PRESSURE_MAX))
        alerts = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Add alert types and convert datetime
        for alert in alerts:
            alert['timestamp'] = alert['timestamp'].isoformat()
            alert['created_at'] = alert['created_at'].isoformat()
            alert['alert_types'] = []
            
            if alert['moisture'] > MOISTURE_THRESHOLD:
                alert['alert_types'].append('high_moisture')
            if alert['acoustic'] > ACOUSTIC_THRESHOLD:
                alert['alert_types'].append('high_acoustic')
            if alert['pressure'] < PRESSURE_MIN:
                alert['alert_types'].append('low_pressure')
            if alert['pressure'] > PRESSURE_MAX:
                alert['alert_types'].append('high_pressure')
        
        return jsonify({
            'count': len(alerts),
            'thresholds': {
                'moisture_max': MOISTURE_THRESHOLD,
                'acoustic_max': ACOUSTIC_THRESHOLD,
                'pressure_min': PRESSURE_MIN,
                'pressure_max': PRESSURE_MAX
            },
            'data': alerts
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/chart-data', methods=['GET'])
def get_chart_data():
    """Get formatted data for charts"""
    hours = request.args.get('hours', default=1, type=int)
    hours = min(hours, 24)
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                timestamp,
                pressure,
                moisture,
                acoustic
            FROM sensor_readings
            WHERE timestamp >= %s
            ORDER BY timestamp ASC
        """, (start_time,))
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Format for Chart.js
        chart_data = {
            'labels': [],
            'pressure': [],
            'moisture': [],
            'acoustic': []
        }
        
        for reading in readings:
            chart_data['labels'].append(reading['timestamp'].strftime('%H:%M:%S'))
            chart_data['pressure'].append(float(reading['pressure']))
            chart_data['moisture'].append(float(reading['moisture']))
            chart_data['acoustic'].append(float(reading['acoustic']))
        
        return jsonify(chart_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 LeakSense Flask Backend Starting...")
    print("=" * 60)
    print(f"Database: {app.config['DB_NAME']}@{app.config['DB_HOST']}")
    print(f"Server: http://0.0.0.0:{app.config['PORT']}")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
