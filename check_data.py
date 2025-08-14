#!/usr/bin/env python3
"""
Check current data in the IoT Data Logger
"""

import requests
import json

def check_data():
    """Check current data in the database"""
    try:
        response = requests.get('http://127.0.0.1:5000/data')
        data = response.json()
        
        print("📊 Current IoT Data Logger Status")
        print("=" * 40)
        print(f"Total data points: {data['count']}")
        
        if data['count'] > 0:
            print("\nLatest readings:")
            for i, reading in enumerate(data['data'][-5:], 1):
                print(f"  {i}. {reading['timestamp']}: {reading['temperature']}°C, {reading['humidity']}%")
        else:
            print("\nNo data available yet.")
            print("Try clicking 'Simulate New Data' on the dashboard or run:")
            print("python auto_simulate.py")
        
        print("\n🌐 Dashboard available at: http://127.0.0.1:5000/")
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("Please start the server with: python app_simple.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_data() 