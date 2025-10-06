import requests
import json

# API base URL
base_url = "http://localhost:5192"

# Tracker mappings (device ID -> actual tracker ID from API)
tracker_mappings = {
    "COW_GPS_ER_01": 4,
    "COW_GPS_ER_02": 6,
    "COW_GPS_ER_03": 7,
    "COW_GPS_ER_04": 8,
    "COW_GPS_ER_05": 9,
    "COW_GPS_ER_06": 10,
    "COW_GPS_ER_07": 11,
    "COW_GPS_ER_08": 12,
    "COW_GPS_ER_09": 13,
    "COW_GPS_ER_10": 14
}

# Animals data
animals = [
    {"name": "Vaca Entre Rios 01", "tag": "ER001", "breed": "Holstein", "gender": "Female", "birthDate": "2021-03-15", "weight": 450.0, "farmId": 7, "trackerId": 4},
    {"name": "Vaca Entre Rios 02", "tag": "ER002", "breed": "Angus", "gender": "Male", "birthDate": "2020-08-22", "weight": 520.0, "farmId": 7, "trackerId": 6},
    {"name": "Vaca Entre Rios 03", "tag": "ER003", "breed": "Holstein", "gender": "Female", "birthDate": "2021-05-10", "weight": 420.0, "farmId": 7, "trackerId": 7},
    {"name": "Vaca Entre Rios 04", "tag": "ER004", "breed": "Brahman", "gender": "Female", "birthDate": "2020-12-05", "weight": 480.0, "farmId": 7, "trackerId": 8},
    {"name": "Vaca Entre Rios 05", "tag": "ER005", "breed": "Angus", "gender": "Male", "birthDate": "2021-01-18", "weight": 510.0, "farmId": 7, "trackerId": 9},
    {"name": "Vaca Entre Rios 06", "tag": "ER006", "breed": "Holstein", "gender": "Female", "birthDate": "2021-04-25", "weight": 440.0, "farmId": 7, "trackerId": 10},
    {"name": "Vaca Entre Rios 07", "tag": "ER007", "breed": "Hereford", "gender": "Male", "birthDate": "2020-09-12", "weight": 495.0, "farmId": 7, "trackerId": 11},
    {"name": "Vaca Entre Rios 08", "tag": "ER008", "breed": "Holstein", "gender": "Female", "birthDate": "2021-06-08", "weight": 415.0, "farmId": 7, "trackerId": 12},
    {"name": "Vaca Entre Rios 09", "tag": "ER009", "breed": "Brahman", "gender": "Female", "birthDate": "2020-11-30", "weight": 465.0, "farmId": 7, "trackerId": 13},
    {"name": "Vaca Entre Rios 10", "tag": "ER010", "breed": "Angus", "gender": "Male", "birthDate": "2021-02-14", "weight": 505.0, "farmId": 7, "trackerId": 14}
]

# Headers for API calls
headers = {
    'Content-Type': 'application/json'
}

print("Creating 10 animals with existing trackers...")

# Create animals
for animal_data in animals:
    try:
        response = requests.post(f"{base_url}/api/Animals", json=animal_data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            print(f"OK Created animal {animal_data['tag']} - {animal_data['name']} with tracker ID {animal_data['trackerId']}")
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