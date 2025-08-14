# 🚀 Quick Start Guide - IoT Data Logger and Visualizer

## ⚡ Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app_simple.py
```

### 3. Open Dashboard
Visit: **http://127.0.0.1:5000/**

## 🎯 What You'll See

- **Real-time Charts**: Temperature and humidity data displayed as live-updating line charts
- **Data Table**: Recent sensor readings in a sortable table
- **Interactive Controls**: Buttons to simulate new data and clear all data
- **Auto-refresh**: Charts update automatically every 5 seconds

## 🔧 Useful Commands

### Check Current Data
```bash
python check_data.py
```

### Test API Endpoints
```bash
python test_app.py
```

### Generate Data Continuously
```bash
python auto_simulate.py 5  # Generate data every 5 seconds
```

### Manual Data Generation
```bash
curl -X POST http://127.0.0.1:5000/simulate
```

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /data` - Get last 10 sensor readings
- `POST /simulate` - Generate new random data
- `GET /clear` - Clear all data

## 🎨 Features

- **Dark Theme**: Modern gradient background with glass-morphism effects
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: No page refresh required
- **Smooth Animations**: Chart updates with smooth transitions

## 🛠️ Troubleshooting

### Server Won't Start
- Make sure port 5000 is not in use
- Try: `python app_simple.py` (simplified version)

### No Data Showing
- Click "Simulate New Data" button
- Or run: `python auto_simulate.py`

### Charts Not Loading
- Check browser console for errors
- Ensure Chart.js CDN is accessible

## 📱 Mobile Friendly

The dashboard is fully responsive and works great on mobile devices!

---

**Happy IoT Monitoring! 🌡️💧** 