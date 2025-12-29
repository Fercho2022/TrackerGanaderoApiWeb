#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear nuevos trackers específicos para la Granja Norte
manteniendo los existentes para Entre Rios
"""

import requests
import json

API_BASE_URL = "http://localhost:5192/api"

def get_all_animals():
    response = requests.get(f"{API_BASE_URL}/Animals")
    response.raise_for_status()
    return response.json()

def create_tracker(device_id, model="GPS Tracker v1.0"):
    """Crea un nuevo tracker"""
    try:
        tracker_data = {
            "deviceId": device_id,
            "model": model,
            "batteryLevel": 100,
            "isActive": True
        }
        response = requests.post(f"{API_BASE_URL}/Trackers",
                               json=tracker_data,
                               headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creando tracker {device_id}: {e}")
        return None

def associate_tracker_with_animal(animal_id, tracker_id):
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
    print("CREACION DE TRACKERS PARA GRANJA NORTE")
    print("=" * 50)

    animals = get_all_animals()

    # Animales de la Granja Norte (Farm ID 8) sin tracker
    farm8_animals = [a for a in animals if a['farmId'] == 8 and a['trackerId'] is None]
    farm8_animals_sorted = sorted(farm8_animals, key=lambda x: x['tag'])

    print(f"Animales sin tracker en Granja Norte: {len(farm8_animals_sorted)}")

    if len(farm8_animals_sorted) == 0:
        print("Todos los animales de Granja Norte ya tienen trackers asignados")
        return

    print(f"\nCreando nuevos trackers para Granja Norte...")
    print("-" * 50)

    trackers_created = 0
    for i, animal in enumerate(farm8_animals_sorted, 1):
        # Crear device IDs únicos para Granja Norte
        device_id = f"COW_NORTH_FARM_{i:02d}"

        print(f"Creando tracker {device_id} para {animal['tag']}")
        new_tracker = create_tracker(device_id)

        if new_tracker:
            tracker_id = new_tracker['id']
            print(f"  Tracker {tracker_id} creado")

            if associate_tracker_with_animal(animal['id'], tracker_id):
                trackers_created += 1
                print(f"  OK - {animal['tag']} asociado con {device_id}")
            else:
                print("  ERROR en asociacion")
        else:
            print("  ERROR creando tracker")

    print(f"\n" + "=" * 50)
    print("RESUMEN:")
    print(f"Nuevos trackers creados para Granja Norte: {trackers_created}")

    print(f"\nAhora necesitas:")
    print("1. Actualizar simple_10_cows_emulator.py para usar los nuevos device IDs:")
    for i in range(1, min(11, trackers_created + 1)):
        print(f"   COW_NORTH_FARM_{i:02d}")

    print(f"\n2. O crear un nuevo emulador específico para Granja Norte")

if __name__ == "__main__":
    main()