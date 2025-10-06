#!/usr/bin/env python3
"""
GPS Emulator for 10 Cows in Entre Ríos, Argentina
Simulates 10 cows with GPS trackers moving in realistic patterns near each other
"""

import requests
import time
import random
import math
import datetime
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CowGPS:
    device_id: str
    name: str
    tag: str
    base_lat: float
    base_lng: float
    current_lat: float
    current_lng: float
    speed: float
    heading: float
    battery_level: int
    temperature: float
    activity_level: int

class MultiCowGPSEmulator:
    def __init__(self, api_base_url: str = "http://localhost:5192"):
        self.api_base_url = api_base_url
        self.cows = self._initialize_cows()

    def _initialize_cows(self) -> List[CowGPS]:
        """Initialize 10 cows with positions around Entre Ríos"""
        # Base coordinates: Entre Ríos, Argentina
        base_lat = -33.0167
        base_lng = -58.5167

        cows = []

        for i in range(1, 11):
            # Spread cows in a 2km radius circle around the base point
            angle = (i - 1) * (360 / 10)  # Distribute evenly in circle
            radius_km = random.uniform(0.2, 1.5)  # Random radius between 200m and 1.5km

            # Convert to lat/lng offset
            lat_offset = (radius_km / 111.32) * math.cos(math.radians(angle))
            lng_offset = (radius_km / (111.32 * math.cos(math.radians(base_lat)))) * math.sin(math.radians(angle))

            cow = CowGPS(
                device_id=f"COW_GPS_ER_{i:02d}",
                name=f"Vaca Entre Ríos {i:02d}",
                tag=f"ER{i:03d}",
                base_lat=base_lat + lat_offset,
                base_lng=base_lng + lng_offset,
                current_lat=base_lat + lat_offset,
                current_lng=base_lng + lng_offset,
                speed=random.uniform(0, 3),
                heading=random.uniform(0, 360),
                battery_level=random.randint(85, 100),
                temperature=random.uniform(36, 40),
                activity_level=random.randint(1, 10)
            )
            cows.append(cow)

        return cows

    def _update_cow_position(self, cow: CowGPS):
        """Update cow position with realistic movement"""
        # Simulate grazing behavior - mostly small movements
        movement_type = random.choices(
            ['graze', 'walk', 'rest'],
            weights=[60, 30, 10]
        )[0]

        if movement_type == 'graze':
            # Small movements while grazing
            speed = random.uniform(0, 0.5)
            heading_change = random.uniform(-45, 45)
        elif movement_type == 'walk':
            # Normal walking
            speed = random.uniform(0.5, 2.5)
            heading_change = random.uniform(-90, 90)
        else:  # rest
            # Minimal movement
            speed = random.uniform(0, 0.1)
            heading_change = random.uniform(-10, 10)

        # Update heading
        cow.heading = (cow.heading + heading_change) % 360
        cow.speed = speed

        # Calculate movement distance (20 seconds * speed)
        distance_km = (speed * 20) / 3600  # Convert km/h to km in 20 seconds

        # Convert to lat/lng movement
        lat_change = (distance_km / 111.32) * math.cos(math.radians(cow.heading))
        lng_change = (distance_km / (111.32 * math.cos(math.radians(cow.current_lat)))) * math.sin(math.radians(cow.heading))

        # Update position
        cow.current_lat += lat_change
        cow.current_lng += lng_change

        # Keep cows within reasonable bounds (3km radius from base)
        dist_from_base = self._calculate_distance(
            cow.current_lat, cow.current_lng,
            cow.base_lat, cow.base_lng
        )

        if dist_from_base > 2.5:  # If too far, head back toward base
            bearing = self._calculate_bearing(
                cow.current_lat, cow.current_lng,
                cow.base_lat, cow.base_lng
            )
            cow.heading = bearing + random.uniform(-30, 30)

        # Update other attributes
        cow.battery_level = max(10, cow.battery_level - random.choice([0, 0, 0, 1]))  # Slow battery drain
        cow.temperature = random.uniform(36, 40)
        cow.activity_level = random.randint(1, 10)

    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlng/2) * math.sin(dlng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def _calculate_bearing(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate bearing from point 1 to point 2"""
        dlng = math.radians(lng2 - lng1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)

        y = math.sin(dlng) * math.cos(lat2_rad)
        x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
             math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlng))

        bearing = math.atan2(y, x)
        return (math.degrees(bearing) + 360) % 360

    def send_gps_data(self, cow: CowGPS) -> bool:
        """Send GPS data to the API"""
        try:
            gps_data = {
                "deviceId": cow.device_id,
                "latitude": cow.current_lat,
                "longitude": cow.current_lng,
                "altitude": random.uniform(15, 30),
                "speed": cow.speed,
                "heading": cow.heading,
                "accuracy": random.uniform(2, 8),
                "batteryLevel": cow.battery_level,
                "temperature": cow.temperature,
                "signalStrength": random.randint(70, 95),
                "activityLevel": cow.activity_level,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }

            response = requests.post(
                f"{self.api_base_url}/api/tracking/tracker-data",
                json=gps_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                print(f"OK {cow.name} - GPS data sent successfully")
                print(f"   Lat: {cow.current_lat:.6f}, Lng: {cow.current_lng:.6f}")
                print(f"   Speed: {cow.speed:.1f} km/h, Activity: {cow.activity_level}/10")
                return True
            else:
                print(f"ERROR {cow.name} - Error: {response.status_code}")
                return False

        except Exception as e:
            print(f"ERROR {cow.name} - Exception: {e}")
            return False

    def run_simulation(self):
        """Run the GPS simulation for all cows"""
        print("Starting GPS simulation for 10 cows in Entre Rios, Argentina")
        print("Base coordinates: -33.0167, -58.5167")
        print("Sending GPS data every 20 seconds...")
        print("-" * 80)

        iteration = 0

        while True:
            try:
                iteration += 1
                print(f"\nIteration {iteration} - {datetime.datetime.now().strftime('%H:%M:%S')}")
                print("-" * 50)

                successful_sends = 0

                for cow in self.cows:
                    # Update cow position
                    self._update_cow_position(cow)

                    # Send GPS data
                    if self.send_gps_data(cow):
                        successful_sends += 1

                    # Small delay between cows to avoid overwhelming the API
                    time.sleep(0.5)

                print(f"\nSummary: {successful_sends}/{len(self.cows)} cows sent data successfully")
                print(f"Next update in 20 seconds...")

                # Wait 20 seconds before next update
                time.sleep(15)  # 15 + (10 cows * 0.5) = ~20 seconds total

            except KeyboardInterrupt:
                print("\nSimulation stopped by user")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    emulator = MultiCowGPSEmulator()
    emulator.run_simulation()