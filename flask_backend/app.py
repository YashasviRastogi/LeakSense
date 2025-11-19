#!/usr/bin/env python3
"""
LeakSense Flask Backend API
Provides REST API for sensor data visualization
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import sqlite3

import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

app = Flask(__name__, 
            static_folder='../web_frontend',
            template_folder='../web_frontend')
app.config.from_object(Config)
CORS(app)

# Database connection
def _ensure_sqlite_schema(conn):
    """Create required tables/indexes for sqlite fallback (idempotent)."""
    create_table = """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pressure REAL NOT NULL,
        moisture REAL NOT NULL,
        acoustic REAL NOT NULL,
        rssi INTEGER,
        snr REAL,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cur = conn.cursor()
        cur.executescript(create_table)
        conn.commit()
    except Exception:
        # For sqlite3, executescript may be unavailable in some cursor wrappers; fallback to execute
        try:
            cur.execute(create_table)
            conn.commit()
        except Exception as e:
            print(f"Failed to ensure sqlite schema: {e}")


def get_db_connection():
    """Attempt to connect to PostgreSQL; if it fails, fall back to SQLite for local development.

    Returns a tuple: (connection, db_type) where db_type is 'postgres' or 'sqlite'.
    """
    # First try PostgreSQL unless DB_TYPE forces sqlite
    if app.config.get('DB_TYPE', 'postgres').lower() == 'sqlite':
        pg_try = False
    else:
        pg_try = True

    if pg_try:
        try:
            conn = psycopg2.connect(
                host=app.config['DB_HOST'],
                port=app.config['DB_PORT'],
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD']
            )
            return conn, 'postgres'
        except psycopg2.Error as e:
            print(f"Postgres connection error: {e} — falling back to SQLite (local dev only)")

    # Fallback to sqlite
    try:
        sqlite_path = app.config.get('SQLITE_PATH') or os.path.join(os.path.dirname(__file__), '..', 'database', 'leaksense.db')
        # Ensure directory exists
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        conn = sqlite3.connect(sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread=False)
        # Use Row factory so rows behave like dicts
        conn.row_factory = sqlite3.Row
        _ensure_sqlite_schema(conn)
        print(f"✅ Connected to SQLite fallback DB: {sqlite_path}")
        return conn, 'sqlite'
    except Exception as e:
        print(f"Database connection error (both postgres and sqlite): {e}")
        return None, None


@app.route('/')
def index():
    """Serve main dashboard page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    conn, db_type = get_db_connection()
    if conn:
        try:
            conn.close()
        except Exception:
            pass
        return jsonify({
            'status': 'healthy',
            'database': db_type,
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
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        if db_type == 'postgres':
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
                # reading is already a dict-like from RealDictCursor
                # Safely convert datetimes
                if isinstance(reading.get('timestamp'), datetime):
                    reading['timestamp'] = reading['timestamp'].isoformat()
                if isinstance(reading.get('created_at'), datetime):
                    reading['created_at'] = reading['created_at'].isoformat()
                return jsonify(reading), 200
            else:
                return jsonify({'message': 'No data available'}), 404

        else:
            # sqlite
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sensor_readings
                ORDER BY timestamp DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                reading = dict(row)
                # timestamp/created_at may already be strings
                for k in ('timestamp', 'created_at'):
                    v = reading.get(k)
                    if isinstance(v, str):
                        reading[k] = v
                    elif isinstance(v, (datetime,)):
                        reading[k] = v.isoformat()
                    else:
                        reading[k] = None
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
    
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        if db_type == 'postgres':
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
                if isinstance(reading.get('timestamp'), datetime):
                    reading['timestamp'] = reading['timestamp'].isoformat()
                if isinstance(reading.get('created_at'), datetime):
                    reading['created_at'] = reading['created_at'].isoformat()

            return jsonify({
                'count': len(readings),
                'data': readings
            }), 200

        else:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sensor_readings
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            results = []
            for row in rows:
                r = dict(row)
                for k in ('timestamp', 'created_at'):
                    v = r.get(k)
                    if isinstance(v, str):
                        r[k] = v
                    elif isinstance(v, datetime):
                        r[k] = v.isoformat()
                    else:
                        r[k] = None
                results.append(r)

            return jsonify({
                'count': len(results),
                'data': results
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/range', methods=['GET'])
def get_readings_by_range():
    """Get sensor readings within a time range"""
    hours = request.args.get('hours', default=24, type=int)
    hours = min(hours, 168)  # Max 7 days
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        if db_type == 'postgres':
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM sensor_readings
                WHERE timestamp >= %s
                ORDER BY timestamp ASC
            """, (start_time,))
            readings = cursor.fetchall()
            cursor.close()
            conn.close()
            for reading in readings:
                if isinstance(reading.get('timestamp'), datetime):
                    reading['timestamp'] = reading['timestamp'].isoformat()
                if isinstance(reading.get('created_at'), datetime):
                    reading['created_at'] = reading['created_at'].isoformat()

            return jsonify({
                'count': len(readings),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'data': readings
            }), 200

        else:
            cursor = conn.cursor()
            # sqlite stores timestamps as text by default
            cursor.execute("""
                SELECT * FROM sensor_readings
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
            """, (start_time,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            results = []
            for row in rows:
                r = dict(row)
                for k in ('timestamp', 'created_at'):
                    v = r.get(k)
                    if isinstance(v, str):
                        r[k] = v
                    elif isinstance(v, datetime):
                        r[k] = v.isoformat()
                    else:
                        r[k] = None
                results.append(r)

            return jsonify({
                'count': len(results),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'data': results
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensors/statistics', methods=['GET'])
def get_statistics():
    """Get statistical summary of sensor data"""
    hours = request.args.get('hours', default=24, type=int)
    hours = min(hours, 168)  # Max 7 days
    
    start_time = datetime.now() - timedelta(hours=hours)
    
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        if db_type == 'postgres':
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
                stats = {k: float(v) if v is not None else None for k, v in stats.items()}
                stats['period_hours'] = hours
                stats['start_time'] = start_time.isoformat()
                stats['end_time'] = datetime.now().isoformat()
                return jsonify(stats), 200
            else:
                return jsonify({'message': 'No data available'}), 404

        else:
            # sqlite: use slightly different SQL (no STDDEV) and placeholder '?'
            cursor = conn.cursor()
            cursor.execute("""
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
                WHERE timestamp >= ?
            """, (start_time,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                stats = {k: (float(row[k]) if row[k] is not None else None) for k in row.keys()}
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
    
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        if db_type == 'postgres':
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
                if isinstance(alert.get('timestamp'), datetime):
                    alert['timestamp'] = alert['timestamp'].isoformat()
                if isinstance(alert.get('created_at'), datetime):
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

        else:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sensor_readings
                WHERE timestamp >= ?
                AND (
                    moisture > ? OR
                    acoustic > ? OR
                    pressure < ? OR
                    pressure > ?
                )
                ORDER BY timestamp DESC
            """, (start_time, MOISTURE_THRESHOLD, ACOUSTIC_THRESHOLD, PRESSURE_MIN, PRESSURE_MAX))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            alerts = []
            for row in rows:
                alert = dict(row)
                for k in ('timestamp', 'created_at'):
                    v = alert.get(k)
                    if isinstance(v, str):
                        alert[k] = v
                    elif isinstance(v, datetime):
                        alert[k] = v.isoformat()
                    else:
                        alert[k] = None
                alert['alert_types'] = []
                if alert.get('moisture', 0) > MOISTURE_THRESHOLD:
                    alert['alert_types'].append('high_moisture')
                if alert.get('acoustic', 0) > ACOUSTIC_THRESHOLD:
                    alert['alert_types'].append('high_acoustic')
                if alert.get('pressure', 0) < PRESSURE_MIN:
                    alert['alert_types'].append('low_pressure')
                if alert.get('pressure', 0) > PRESSURE_MAX:
                    alert['alert_types'].append('high_pressure')
                alerts.append(alert)

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
    
    conn, db_type = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        chart_data = {
            'labels': [],
            'pressure': [],
            'moisture': [],
            'acoustic': []
        }

        if db_type == 'postgres':
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

            for reading in readings:
                ts = reading.get('timestamp')
                if isinstance(ts, datetime):
                    chart_data['labels'].append(ts.strftime('%H:%M:%S'))
                else:
                    chart_data['labels'].append(str(ts))
                chart_data['pressure'].append(float(reading.get('pressure') or 0))
                chart_data['moisture'].append(float(reading.get('moisture') or 0))
                chart_data['acoustic'].append(float(reading.get('acoustic') or 0))

            return jsonify(chart_data), 200

        else:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    timestamp,
                    pressure,
                    moisture,
                    acoustic
                FROM sensor_readings
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
            """, (start_time,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in rows:
                r = dict(row)
                ts = r.get('timestamp')
                if isinstance(ts, str):
                    # assume already formatted
                    chart_data['labels'].append(ts)
                elif isinstance(ts, datetime):
                    chart_data['labels'].append(ts.strftime('%H:%M:%S'))
                else:
                    chart_data['labels'].append('')
                chart_data['pressure'].append(float(r.get('pressure') or 0))
                chart_data['moisture'].append(float(r.get('moisture') or 0))
                chart_data['acoustic'].append(float(r.get('acoustic') or 0))

            return jsonify(chart_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Static file routes
@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)


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
