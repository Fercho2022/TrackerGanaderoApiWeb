#!/usr/bin/env python3
"""
Setup script to create 10 cows with GPS trackers for testing
Uses the API to create animals and trackers automatically
"""

import requests
import json
import time

def create_animal_via_api(animal_data):
    """Create an animal via API - for demonstration, we'll simulate this"""
    # Since we don't have a direct animal creation endpoint exposed,
    # we'll create this data by sending tracker data first, which will auto-create the relationships
    return True

def main():
    print("🐄 Setting up 10 cows with GPS trackers for Entre Ríos farm")
    print("📡 This will create tracker data that automatically creates animal relationships")
    print("-" * 80)

    # Define 10 cows with initial positions around Entre Ríos
    base_lat = -33.0167
    base_lng = -58.5167

    cows_data = [
        {"device_id": "COW_GPS_ER_01", "name": "Vaca Entre Ríos 01", "tag": "GPS-ER-001", "lat_offset": 0.002, "lng_offset": 0.001},
        {"device_id": "COW_GPS_ER_02", "name": "Vaca Entre Ríos 02", "tag": "GPS-ER-002", "lat_offset": -0.001, "lng_offset": 0.003},
        {"device_id": "COW_GPS_ER_03", "name": "Vaca Entre Ríos 03", "tag": "GPS-ER-003", "lat_offset": 0.003, "lng_offset": -0.002},
        {"device_id": "COW_GPS_ER_04", "name": "Vaca Entre Ríos 04", "tag": "GPS-ER-004", "lat_offset": -0.002, "lng_offset": -0.001},
        {"device_id": "COW_GPS_ER_05", "name": "Vaca Entre Ríos 05", "tag": "GPS-ER-005", "lat_offset": 0.001, "lng_offset": 0.004},
        {"device_id": "COW_GPS_ER_06", "name": "Vaca Entre Ríos 06", "tag": "GPS-ER-006", "lat_offset": -0.003, "lng_offset": 0.002},
        {"device_id": "COW_GPS_ER_07", "name": "Vaca Entre Ríos 07", "tag": "GPS-ER-007", "lat_offset": 0.004, "lng_offset": -0.003},
        {"device_id": "COW_GPS_ER_08", "name": "Vaca Entre Ríos 08", "tag": "GPS-ER-008", "lat_offset": -0.001, "lng_offset": -0.004},
        {"device_id": "COW_GPS_ER_09", "name": "Vaca Entre Ríos 09", "tag": "GPS-ER-009", "lat_offset": 0.005, "lng_offset": 0.001},
        {"device_id": "COW_GPS_ER_10", "name": "Vaca Entre Ríos 10", "tag": "GPS-ER-010", "lat_offset": -0.004, "lng_offset": 0.005},
    ]

    api_base = "http://localhost:5192"

    print("Sending initial GPS data for each cow to establish tracker relationships...")

    for i, cow in enumerate(cows_data, 1):
        try:
            # Initial GPS data for each cow
            gps_data = {
                "deviceId": cow["device_id"],
                "latitude": base_lat + cow["lat_offset"],
                "longitude": base_lng + cow["lng_offset"],
                "altitude": 20.0,
                "speed": 0.0,
                "heading": 0.0,
                "accuracy": 5.0,
                "batteryLevel": 95,
                "temperature": 38.5,
                "signalStrength": 85,
                "activityLevel": 3,
                "timestamp": "2025-10-02T12:00:00.000Z"
            }

            response = requests.post(
                f"{api_base}/api/tracking/tracker-data",
                json=gps_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                print(f"✅ {i:2d}/10 - {cow['name']} ({cow['device_id']}) - GPS data sent successfully")
                print(f"      📍 Position: {base_lat + cow['lat_offset']:.6f}, {base_lng + cow['lng_offset']:.6f}")
            else:
                print(f"❌ {i:2d}/10 - {cow['name']} - Error: {response.status_code}")
                print(f"      Response: {response.text}")

            # Small delay between requests
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ {i:2d}/10 - {cow['name']} - Exception: {e}")

    print("\n" + "="*80)
    print("🎯 Setup complete! Now test the API to see the animals:")
    print("   📡 API endpoint: GET http://localhost:5192/api/Tracking/farm/7/animals")
    print("   🗺️  Open test_map.html in browser to see them on the map")
    print("   🐄 Run emulator_10_cows.py for continuous GPS simulation")
    print("="*80)

if __name__ == "__main__":
    main()