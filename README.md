# 🌡️ IoT Data Logger and Visualizer

A complete Python Flask web application that simulates IoT sensor readings (temperature and humidity), logs them into a SQLite database, and displays them on a live-updating web dashboard using Chart.js.

## 🚀 Features

- **Real-time Data Visualization**: Live-updating charts for temperature and humidity readings
- **SQLite Database**: Persistent storage of sensor data with SQLAlchemy ORM
- **RESTful API**: JSON endpoints for data retrieval and simulation
- **Responsive Design**: Modern dark theme UI that works on all devices
- **Auto-refresh**: Charts update automatically every 5 seconds
- **Interactive Controls**: Manual data simulation and data clearing capabilities

## 📁 Project Structure

```
iot_logger/
├── app_simple.py          # Simplified Flask application (recommended)
├── app.py                 # Original Flask application with SQLAlchemy
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── test_app.py           # Test script for API endpoints
├── check_data.py         # Script to check current data
├── auto_simulate.py      # Automatic data generation script
├── templates/
│   └── index.html        # Main dashboard template
├── static/
│   ├── css/
│   │   └── style.css     # Dark theme styling
│   └── js/
│       └── script.js     # Interactive JavaScript functionality
└── data.db               # SQLite database (created automatically)
```

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application** (choose one):
   ```bash
   # Option 1: Use the simplified version (recommended for Python 3.13+)
   python app_simple.py
   
   # Option 2: Use the original version (if you have compatible SQLAlchemy)
   python app.py
   ```

4. **Open your browser** and visit:
   ```
   http://127.0.0.1:5000/
   ```

## 🎯 Usage

### Dashboard Features

- **View Real-time Charts**: Temperature and humidity data displayed as line charts
- **Data Table**: Recent sensor readings in a sortable table format
- **Status Information**: Last update time and data point count

### API Endpoints

- `GET /` - Main dashboard page
- `GET /data` - Returns last 10 sensor readings in JSON format
- `POST /simulate` - Generates and stores new random sensor data
- `GET /clear` - Clears all data from the database

### Manual Data Generation

1. **Click "Simulate New Data"** button to generate random readings
2. **Visit `/simulate`** directly in your browser
3. **Use curl** to simulate data:
   ```bash
   curl -X POST http://127.0.0.1:5000/simulate
   ```

### Automatic Data Generation

For continuous data generation, you can create a background script:

```python
import requests
import time
import random

while True:
    try:
        response = requests.post('http://127.0.0.1:5000/simulate')
        print(f"Data generated: {response.json()}")
        time.sleep(5)  # Wait 5 seconds between readings
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
```

## 📊 Data Specifications

### Sensor Data Model
- **Temperature**: Random values between 20-30°C
- **Humidity**: Random values between 40-60%
- **Timestamp**: Current UTC time when data is generated

### Database Schema
```sql
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL
);
```

## 🎨 UI Features

- **Dark Theme**: Modern gradient background with glass-morphism effects
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Chart updates with smooth transitions
- **Interactive Elements**: Hover effects and button animations
- **Real-time Updates**: No page refresh required

## 🔧 Technical Details

### Backend Technologies
- **Flask 3.0.0**: Web framework
- **SQLite3**: Direct database access (no ORM dependency)
- **Python 3.13+ compatible**: Works with latest Python versions

### Frontend Technologies
- **Chart.js**: Interactive charts via CDN
- **Vanilla JavaScript**: No framework dependencies
- **CSS3**: Modern styling with gradients and animations

### Database
- **SQLite**: Lightweight, file-based database
- **Automatic Setup**: Database and tables created on first run

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

2. **Database errors**:
   ```bash
   # Delete data.db and restart
   rm data.db
   python app.py
   ```

3. **Chart not loading**:
   - Check browser console for JavaScript errors
   - Ensure Chart.js CDN is accessible
   - Verify all static files are in correct locations

### Debug Mode

The application runs in debug mode by default. For production:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📈 Performance

- **Database**: Optimized queries with proper indexing
- **Frontend**: Efficient DOM updates and memory management
- **Auto-refresh**: Smart interval management (pauses when tab is inactive)

## 🔒 Security Notes

- This is a development/demo application
- No authentication or input validation implemented
- Database file should be protected in production
- Consider adding rate limiting for `/simulate` endpoint

## 🤝 Contributing

Feel free to enhance this project with:
- Additional sensor types
- Export functionality
- User authentication
- Advanced analytics
- Mobile app integration

## 📄 License

This project is open source and available under the MIT License.

---

**Happy IoT Monitoring! 🌡️💧** 