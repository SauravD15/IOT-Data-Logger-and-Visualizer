#!/usr/bin/env python3
"""
Startup script for IoT Data Logger Flask application
"""

import sys
import os

def main():
    """Start the Flask application"""
    print("🚀 Starting IoT Data Logger Flask Application...")
    print("=" * 50)
    
    try:
        # Import the Flask app
        from app import app, init_db
        
        # Initialize database
        print("📊 Initializing database...")
        init_db()
        print("✅ Database initialized successfully!")
        
        # Start the server
        print("🌐 Starting Flask server...")
        print("📍 Server will be available at: http://127.0.0.1:5000/")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 