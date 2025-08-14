#!/usr/bin/env python3
"""
Auto Simulate Script for IoT Data Logger

This script automatically generates sensor data every few seconds
to simulate continuous IoT sensor readings.

Usage:
    python auto_simulate.py [interval_seconds]

Example:
    python auto_simulate.py 5  # Generate data every 5 seconds
"""

import requests
import time
import sys
import signal
import datetime

# Configuration
DEFAULT_INTERVAL = 5  # seconds
API_BASE_URL = "http://127.0.0.1:5000"
SIMULATE_ENDPOINT = f"{API_BASE_URL}/simulate"

# Note: This script works with both app.py and app_simple.py

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n🛑 Shutting down auto-simulate script...")
    running = False

def check_server_status():
    """Check if the Flask server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/data", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def simulate_data():
    """Send a POST request to simulate new sensor data"""
    try:
        response = requests.post(SIMULATE_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                sensor_data = data.get('data', {})
                timestamp = sensor_data.get('timestamp', 'Unknown')
                temp = sensor_data.get('temperature', 0)
                humidity = sensor_data.get('humidity', 0)
                print(f"✅ [{datetime.datetime.now().strftime('%H:%M:%S')}] "
                      f"Data generated - Temp: {temp}°C, Humidity: {humidity}%")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("⏰ Timeout: Server took too long to respond")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Connection Error: Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function to run the auto-simulate loop"""
    # Parse command line arguments
    interval = DEFAULT_INTERVAL
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 1:
                print("⚠️  Interval must be at least 1 second. Using default.")
                interval = DEFAULT_INTERVAL
        except ValueError:
            print("⚠️  Invalid interval. Using default.")
            interval = DEFAULT_INTERVAL

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🚀 IoT Data Logger - Auto Simulate Script")
    print(f"📡 Target: {API_BASE_URL}")
    print(f"⏱️  Interval: {interval} seconds")
    print("=" * 50)

    # Check if server is running
    if not check_server_status():
        print("❌ Error: Flask server is not running!")
        print("Please start the server first with: python app.py")
        return

    print("✅ Server is running. Starting auto-simulation...")
    print("Press Ctrl+C to stop\n")

    success_count = 0
    error_count = 0
    start_time = time.time()

    while running:
        try:
            if simulate_data():
                success_count += 1
            else:
                error_count += 1

            # Print statistics every 10 successful requests
            if success_count % 10 == 0 and success_count > 0:
                elapsed = time.time() - start_time
                rate = success_count / elapsed if elapsed > 0 else 0
                print(f"\n📊 Statistics: {success_count} successful, {error_count} errors")
                print(f"📈 Rate: {rate:.2f} requests/second\n")

            # Wait for next interval
            time.sleep(interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Unexpected error in main loop: {e}")
            time.sleep(interval)

    # Final statistics
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print("📊 Final Statistics:")
    print(f"   Total time: {total_time:.1f} seconds")
    print(f"   Successful requests: {success_count}")
    print(f"   Failed requests: {error_count}")
    print(f"   Success rate: {(success_count/(success_count+error_count)*100):.1f}%" if (success_count+error_count) > 0 else "   Success rate: 0%")
    print("👋 Auto-simulate script stopped.")

if __name__ == "__main__":
    main() 