from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the SensorData model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convert model instance to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': self.temperature,
            'humidity': self.humidity
        }

# Create database tables
def init_db():
    """Initialize the database and create tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/data')
def get_data():
    """API endpoint to get the last 10 sensor readings"""
    try:
        # Get the last 10 readings ordered by timestamp (newest first)
        readings = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()
        
        # Convert to list of dictionaries and reverse to show chronological order
        data = [reading.to_dict() for reading in readings]
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
        
        # Create new sensor reading
        new_reading = SensorData(
            temperature=temperature,
            humidity=humidity,
            timestamp=datetime.utcnow()
        )
        
        # Save to database
        db.session.add(new_reading)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Data simulated successfully',
            'data': new_reading.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clear')
def clear_data():
    """Clear all data from the database (for testing purposes)"""
    try:
        SensorData.query.delete()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'All data cleared successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000) 