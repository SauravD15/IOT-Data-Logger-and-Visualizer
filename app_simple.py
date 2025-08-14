from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import random
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
DATABASE = 'data.db'

def init_db():
    """Initialize the database and create tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create sensor_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            temperature FLOAT NOT NULL,
            humidity FLOAT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def sensor_data_to_dict(row):
    """Convert database row to dictionary"""
    return {
        'id': row['id'],
        'timestamp': row['timestamp'],
        'temperature': row['temperature'],
        'humidity': row['humidity']
    }

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/data')
def get_data():
    """API endpoint to get the last 10 sensor readings"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get the last 10 readings ordered by timestamp (newest first)
        cursor.execute('''
            SELECT id, timestamp, temperature, humidity 
            FROM sensor_data 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        
        readings = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries and reverse to show chronological order
        data = [sensor_data_to_dict(row) for row in readings]
        data.reverse()  # Show oldest to newest for chart display
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/simulate', methods=['GET', 'POST'])
def simulate_data():
    """Generate and store random sensor data"""
    try:
        # Generate random temperature (20-30°C) and humidity (40-60%)
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, temperature, humidity)
            VALUES (?, ?, ?)
        ''', (timestamp, temperature, humidity))
        
        # Get the inserted data
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        new_reading = {
            'id': new_id,
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity
        }
        
        return jsonify({
            'success': True,
            'message': 'Data simulated successfully',
            'data': new_reading
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clear')
def clear_data():
    """Clear all data from the database (for testing purposes)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sensor_data')
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'All data cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000) 