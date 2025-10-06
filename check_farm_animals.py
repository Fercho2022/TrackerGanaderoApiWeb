#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar los trackers y animales en cada granja
"""

import requests

def check_farm_animals():
    """Verifica los animales y trackers en cada granja"""

    # Verificar Granja Norte (ID 8)
    print("=== GRANJA NORTE (ID 8) ===")
    try:
        response = requests.get("http://localhost:5192/api/Tracking/farm/8/animals", timeout=10)
        if response.status_code == 200:
            animals = response.json()
            print(f"Animales encontrados: {len(animals)}")
            for animal in animals:
                print(f"  - {animal['tag']}: {animal['name']} (Tracker: {animal.get('tracker', {}).get('deviceId', 'N/A')})")
                if animal.get('currentLocation'):
                    loc = animal['currentLocation']
                    print(f"    Última ubicación: {loc['latitude']:.6f}, {loc['longitude']:.6f} ({loc['timestamp']})")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*60 + "\n")

    # Verificar Entre Ríos (ID 7)
    print("=== ENTRE RIOS - VACA GP (ID 7) ===")
    try:
        response = requests.get("http://localhost:5192/api/Tracking/farm/7/animals", timeout=10)
        if response.status_code == 200:
            animals = response.json()
            print(f"Animales encontrados: {len(animals)}")
            for animal in animals:
                print(f"  - {animal['tag']}: {animal['name']} (Tracker: {animal.get('tracker', {}).get('deviceId', 'N/A')})")
                if animal.get('currentLocation'):
                    loc = animal['currentLocation']
                    print(f"    Última ubicación: {loc['latitude']:.6f}, {loc['longitude']:.6f} ({loc['timestamp']})")
                else:
                    print("    Sin ubicación actual")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_farm_animals()