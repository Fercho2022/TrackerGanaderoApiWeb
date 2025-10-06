#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar todos los trackers, animales y sus relaciones
"""

import requests
import json

def check_all_trackers():
    """Verifica todos los trackers disponibles"""

    print("=== VERIFICACION COMPLETA DE TRACKERS Y ANIMALES ===\n")

    # Obtener todos los trackers
    try:
        response = requests.get("http://localhost:5192/api/trackers", timeout=10)
        if response.status_code == 200:
            trackers = response.json()
            print(f"TOTAL DE TRACKERS: {len(trackers)}")
            print("-" * 60)
            for tracker in trackers:
                print(f"ID: {tracker['id']} | DeviceId: {tracker['deviceId']} | Activo: {tracker['isActive']}")
                print(f"  Modelo: {tracker.get('model', 'N/A')} | Batería: {tracker.get('batteryLevel', 'N/A')}%")
                print(f"  Última señal: {tracker.get('lastSeen', 'N/A')}")
                print()
        else:
            print(f"Error obteniendo trackers: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*60 + "\n")

    # Obtener todos los animales
    try:
        response = requests.get("http://localhost:5192/api/animals", timeout=10)
        if response.status_code == 200:
            animals = response.json()
            print(f"TOTAL DE ANIMALES: {len(animals)}")
            print("-" * 60)
            for animal in animals:
                print(f"ID: {animal['id']} | Tag: {animal['tag']} | Nombre: {animal['name']}")
                print(f"  Granja ID: {animal['farmId']} | Tracker ID: {animal.get('trackerId', 'SIN TRACKER')}")
                print()
        else:
            print(f"Error obteniendo animales: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "="*60 + "\n")

    # Verificar relaciones tracker-animal por granja
    granjas = [7, 8]  # Entre Ríos y Granja Norte

    for granja_id in granjas:
        nombre_granja = "Entre Ríos - Vaca GP" if granja_id == 7 else "Granja Norte"
        print(f"=== {nombre_granja.upper()} (ID {granja_id}) ===")

        try:
            response = requests.get(f"http://localhost:5192/api/Tracking/farm/{granja_id}/animals", timeout=10)
            if response.status_code == 200:
                animals = response.json()
                print(f"Animales con tracker: {len(animals)}")

                for animal in animals:
                    tracker_info = animal.get('tracker', {})
                    device_id = tracker_info.get('deviceId', 'N/A')
                    last_seen = tracker_info.get('lastSeen', 'N/A')

                    location = animal.get('currentLocation')
                    if location:
                        loc_time = location.get('timestamp', 'N/A')
                        coords = f"{location['latitude']:.6f}, {location['longitude']:.6f}"
                    else:
                        loc_time = "SIN UBICACION"
                        coords = "N/A"

                    print(f"  {animal['tag']}: {animal['name']}")
                    print(f"    Tracker: {device_id} | Última señal: {last_seen}")
                    print(f"    Ubicación: {coords} | Tiempo: {loc_time}")
                    print()
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        print("-" * 60 + "\n")

if __name__ == "__main__":
    check_all_trackers()