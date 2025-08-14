#!/usr/bin/env python3
"""
Test script for IoT Data Logger Flask application
"""

import requests
import time
import json

def test_server():
    """Test the Flask server endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing IoT Data Logger Flask Application")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/data", timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running. Please start with: python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Get initial data
    print("2. Testing /data endpoint...")
    try:
        response = requests.get(f"{base_url}/data")
        data = response.json()
        print(f"   ✅ Data endpoint working (Count: {data.get('count', 0)})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Simulate new data
    print("3. Testing /simulate endpoint...")
    try:
        response = requests.post(f"{base_url}/simulate")
        data = response.json()
        if data.get('success'):
            sensor_data = data.get('data', {})
            print(f"   ✅ Data simulated successfully")
            print(f"      Temperature: {sensor_data.get('temperature')}°C")
            print(f"      Humidity: {sensor_data.get('humidity')}%")
        else:
            print(f"   ❌ Error: {data.get('error')}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Get updated data
    print("4. Testing updated data...")
    try:
        response = requests.get(f"{base_url}/data")
        data = response.json()
        print(f"   ✅ Updated data retrieved (Count: {data.get('count', 0)})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n🎉 All tests passed! The application is working correctly.")
    print("\n📋 Next steps:")
    print("   1. Open your browser and visit: http://127.0.0.1:5000/")
    print("   2. Use the dashboard to view real-time charts")
    print("   3. Click 'Simulate New Data' to generate more readings")
    print("   4. Run 'python auto_simulate.py' for continuous data generation")
    
    return True

if __name__ == "__main__":
    test_server() 