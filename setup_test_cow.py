import requests
import json

# API base URL
base_url = "http://localhost:5192"

# Create 10 trackers
trackers = [
    {"deviceId": "COW_GPS_ER_01", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_02", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_03", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_04", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_05", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_06", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_07", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_08", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_09", "model": "GPS Tracker v1.0"},
    {"deviceId": "COW_GPS_ER_10", "model": "GPS Tracker v1.0"}
]

# Animals data
animals = [
    {"name": "Vaca Entre Rios 01", "tag": "ER001", "breed": "Holstein", "gender": "Female", "birthDate": "2021-03-15", "weight": 450.0, "farmId": 7},
    {"name": "Vaca Entre Rios 02", "tag": "ER002", "breed": "Angus", "gender": "Male", "birthDate": "2020-08-22", "weight": 520.0, "farmId": 7},
    {"name": "Vaca Entre Rios 03", "tag": "ER003", "breed": "Holstein", "gender": "Female", "birthDate": "2021-05-10", "weight": 420.0, "farmId": 7},
    {"name": "Vaca Entre Rios 04", "tag": "ER004", "breed": "Brahman", "gender": "Female", "birthDate": "2020-12-05", "weight": 480.0, "farmId": 7},
    {"name": "Vaca Entre Rios 05", "tag": "ER005", "breed": "Angus", "gender": "Male", "birthDate": "2021-01-18", "weight": 510.0, "farmId": 7},
    {"name": "Vaca Entre Rios 06", "tag": "ER006", "breed": "Holstein", "gender": "Female", "birthDate": "2021-04-25", "weight": 440.0, "farmId": 7},
    {"name": "Vaca Entre Rios 07", "tag": "ER007", "breed": "Hereford", "gender": "Male", "birthDate": "2020-09-12", "weight": 495.0, "farmId": 7},
    {"name": "Vaca Entre Rios 08", "tag": "ER008", "breed": "Holstein", "gender": "Female", "birthDate": "2021-06-08", "weight": 415.0, "farmId": 7},
    {"name": "Vaca Entre Rios 09", "tag": "ER009", "breed": "Brahman", "gender": "Female", "birthDate": "2020-11-30", "weight": 465.0, "farmId": 7},
    {"name": "Vaca Entre Rios 10", "tag": "ER010", "breed": "Angus", "gender": "Male", "birthDate": "2021-02-14", "weight": 505.0, "farmId": 7}
]

# Headers for API calls
headers = {
    'Content-Type': 'application/json'
}

print("Creating 10 trackers...")
tracker_ids = {}

# Create trackers
for i, tracker_data in enumerate(trackers):
    try:
        response = requests.post(f"{base_url}/api/Trackers", json=tracker_data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            tracker_ids[tracker_data["deviceId"]] = result["id"]
            print(f"OK Created tracker {tracker_data['deviceId']} with ID {result['id']}")
        else:
            print(f"FAIL Failed to create tracker {tracker_data['deviceId']}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR Error creating tracker {tracker_data['deviceId']}: {str(e)}")

print(f"\nCreated {len(tracker_ids)} trackers")

print("\nCreating 10 animals...")

# Create animals with tracker IDs
for i, animal_data in enumerate(animals):
    device_id = f"COW_GPS_ER_{i+1:02d}"
    if device_id in tracker_ids:
        # Update the animal data to include tracker assignment
        animal_with_tracker = animal_data.copy()
        animal_with_tracker["trackerId"] = tracker_ids[device_id]
    else:
        animal_with_tracker = animal_data.copy()
        print(f"WARNING: No tracker found for {device_id}")

    try:
        response = requests.post(f"{base_url}/api/Animals", json=animal_with_tracker, headers=headers)
        if response.status_code == 201:
            result = response.json()
            print(f"OK Created animal {animal_data['tag']} - {animal_data['name']} with tracker {device_id}")
        else:
            print(f"FAIL Failed to create animal {animal_data['tag']}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"ERROR Error creating animal {animal_data['tag']}: {str(e)}")

print("\nSetup complete! Testing API endpoint...")

# Test the farm animals endpoint
try:
    response = requests.get(f"{base_url}/api/Tracking/farm/7/animals")
    if response.status_code == 200:
        animals_data = response.json()
        print(f"OK Farm 7 now has {len(animals_data)} animals with GPS trackers")
        for animal in animals_data:
            print(f"  - {animal['name']} ({animal['tag']}) - Tracker: {animal.get('trackerId', 'N/A')}")
    else:
        print(f"FAIL Failed to test endpoint: {response.status_code}")
except Exception as e:
    print(f"ERROR Error testing endpoint: {str(e)}")