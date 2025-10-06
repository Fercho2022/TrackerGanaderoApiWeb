#!/usr/bin/env python3
"""
Test simple del emulador GPS para debug
"""

import requests
import json

def test_single_cow():
    """Test enviando datos de una sola vaca"""
    print("Testing emulator with single cow...")

    # Datos de prueba para ER001
    test_data = {
        "deviceId": "COW_GPS_ER_01",
        "latitude": -33.0167,
        "longitude": -58.5167,
        "altitude": 20.0,
        "speed": 1.5,
        "activityLevel": 5,
        "temperature": 38.2,
        "timestamp": "2025-10-03T18:55:00.000Z"
    }

    try:
        print(f"Sending data for {test_data['deviceId']}...")
        print(f"Data: {json.dumps(test_data, indent=2)}")

        response = requests.post(
            "http://localhost:5192/api/tracking/tracker-data",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Data sent successfully!")
            return True
        else:
            print(f"ERROR: Status {response.status_code}")
            return False

    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    test_single_cow()