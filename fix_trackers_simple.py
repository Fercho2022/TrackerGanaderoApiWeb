#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solucion simple para liberar y reasignar trackers GPS-ER
"""

import requests
import json

API_BASE_URL = "http://localhost:5192/api"

def liberar_tracker_de_animal(animal_id):
    """Libera un tracker de un animal estableciendo trackerId a null"""
    try:
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        update_data = {
            "name": animal_data["name"],
            "tag": animal_data["tag"],
            "birthDate": animal_data["birthDate"],
            "gender": animal_data["gender"],
            "breed": animal_data["breed"],
            "weight": animal_data["weight"],
            "status": animal_data["status"],
            "farmId": animal_data["farmId"],
            "trackerId": None
        }

        response = requests.put(f"{API_BASE_URL}/Animals/{animal_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error liberando tracker: {e}")
        return False

def asociar_tracker_a_animal(animal_id, tracker_id):
    """Asocia un tracker con un animal"""
    try:
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        update_data = {
            "name": animal_data["name"],
            "tag": animal_data["tag"],
            "birthDate": animal_data["birthDate"],
            "gender": animal_data["gender"],
            "breed": animal_data["breed"],
            "weight": animal_data["weight"],
            "status": animal_data["status"],
            "farmId": animal_data["farmId"],
            "trackerId": tracker_id
        }

        response = requests.put(f"{API_BASE_URL}/Animals/{animal_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error asociando tracker: {e}")
        return False

def main():
    print("REASIGNACION DE TRACKERS GPS-ER")
    print("=" * 50)

    # Obtener todos los animales y trackers
    animals_response = requests.get(f"{API_BASE_URL}/Animals")
    animals = animals_response.json()

    trackers_response = requests.get(f"{API_BASE_URL}/Trackers")
    trackers = trackers_response.json()

    # Animales GPS-ER de la granja 7
    gps_er_animals = [a for a in animals if a['farmId'] == 7 and a['tag'].startswith('GPS-ER-')]
    gps_er_animals.sort(key=lambda x: x['tag'])

    # Trackers COW_GPS_ER
    gps_er_trackers = {t['deviceId']: t for t in trackers if t['deviceId'].startswith('COW_GPS_ER_')}

    # Animales de granja 8 con trackers COW_GPS_ER
    farm8_animals = []
    for animal in animals:
        if animal['farmId'] == 8 and animal['trackerId']:
            tracker = next((t for t in trackers if t['id'] == animal['trackerId']), None)
            if tracker and tracker['deviceId'].startswith('COW_GPS_ER_'):
                farm8_animals.append(animal)

    print(f"Paso 1: Liberando {len(farm8_animals)} trackers de granja 8")

    liberados = 0
    for animal in farm8_animals:
        tracker = next((t for t in trackers if t['id'] == animal['trackerId']), None)
        if tracker:
            print(f"Liberando {tracker['deviceId']} del animal {animal['tag']}")
            if liberar_tracker_de_animal(animal['id']):
                liberados += 1
                print("  OK - Liberado")
            else:
                print("  ERROR")

    print(f"\nPaso 2: Asociando trackers con animales GPS-ER")

    asociados = 0
    for animal in gps_er_animals:
        tag = animal['tag']
        if tag.startswith('GPS-ER-'):
            tag_number = int(tag.split('-')[-1])
            device_id = f"COW_GPS_ER_{tag_number:02d}"

            if device_id in gps_er_trackers:
                tracker_id = gps_er_trackers[device_id]['id']
                print(f"Asociando {tag} -> {device_id}")
                if asociar_tracker_a_animal(animal['id'], tracker_id):
                    asociados += 1
                    print("  OK - Asociado")
                else:
                    print("  ERROR")

    print(f"\nRESUMEN:")
    print(f"Trackers liberados: {liberados}")
    print(f"Asociaciones realizadas: {asociados}")
    print(f"Total animales GPS-ER: {len(gps_er_animals)}")

if __name__ == "__main__":
    main()