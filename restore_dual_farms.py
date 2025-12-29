#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para restaurar el funcionamiento dual de ambas granjas:
- Granja Norte (Farm ID 8): 10 animales con simple_10_cows_emulator.py
- Entre Rios - Vaca GPS (Farm ID 7): 15 animales con start_emulator_5192.py
"""

import requests
import json

API_BASE_URL = "http://localhost:5192/api"

def get_all_animals():
    response = requests.get(f"{API_BASE_URL}/Animals")
    response.raise_for_status()
    return response.json()

def get_all_trackers():
    response = requests.get(f"{API_BASE_URL}/Trackers")
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
        print(f"Error asociando tracker con animal {animal_id}: {e}")
        return False

def main():
    print("RESTAURACION DE FUNCIONAMIENTO DUAL DE GRANJAS")
    print("=" * 60)

    animals = get_all_animals()
    trackers = get_all_trackers()

    # Filtrar animales por granja
    farm8_animals = [a for a in animals if a['farmId'] == 8]  # Granja Norte
    farm7_animals = [a for a in animals if a['farmId'] == 7 and a['tag'].startswith('GPS-ER-')]  # Entre Rios

    print(f"Animales en Granja Norte (Farm 8): {len(farm8_animals)}")
    print(f"Animales GPS-ER en Entre Rios (Farm 7): {len(farm7_animals)}")

    # Crear mapeo de device IDs existentes
    existing_trackers = {t['deviceId']: t for t in trackers}

    print(f"\nPASO 1: Restaurando trackers para Granja Norte (10 animales)")
    print("-" * 60)

    # Restaurar trackers para Granja Norte (COW_GPS_ER_01 a COW_GPS_ER_10)
    farm8_restored = 0
    farm8_animals_sorted = sorted(farm8_animals, key=lambda x: x['tag'])

    for i, animal in enumerate(farm8_animals_sorted[:10], 1):
        device_id = f"COW_GPS_ER_{i:02d}"

        if device_id in existing_trackers:
            tracker_id = existing_trackers[device_id]['id']
            print(f"Restaurando {animal['tag']} -> {device_id} (Tracker {tracker_id})")
            if associate_tracker_with_animal(animal['id'], tracker_id):
                farm8_restored += 1
                print("  OK - Restaurado")
            else:
                print("  ERROR")
        else:
            print(f"Tracker {device_id} no encontrado para {animal['tag']}")

    print(f"\nPASO 2: Creando nuevos trackers para animales GPS-ER faltantes")
    print("-" * 60)

    # Crear nuevos trackers para GPS-ER que no tienen tracker asignado
    gps_er_created = 0
    farm7_animals_sorted = sorted(farm7_animals, key=lambda x: x['tag'])

    for animal in farm7_animals_sorted:
        if animal['trackerId'] is None:
            tag = animal['tag']
            if tag.startswith('GPS-ER-'):
                tag_number = int(tag.split('-')[-1])
                new_device_id = f"COW_GPS_ER_NEW_{tag_number:02d}"

                print(f"Creando nuevo tracker {new_device_id} para {tag}")
                new_tracker = create_tracker(new_device_id)

                if new_tracker:
                    tracker_id = new_tracker['id']
                    print(f"  Tracker {tracker_id} creado")

                    if associate_tracker_with_animal(animal['id'], tracker_id):
                        gps_er_created += 1
                        print("  OK - Asociado")
                    else:
                        print("  ERROR en asociacion")
                else:
                    print("  ERROR creando tracker")

    print(f"\nPASO 3: Verificando trackers ya asociados correctamente")
    print("-" * 60)

    gps_er_existing = 0
    for animal in farm7_animals_sorted:
        if animal['trackerId'] is not None:
            gps_er_existing += 1
            print(f"YA ASOCIADO: {animal['tag']} -> Tracker {animal['trackerId']}")

    print(f"\n" + "=" * 60)
    print("RESUMEN FINAL:")
    print(f"Granja Norte restaurada: {farm8_restored}/10 animales")
    print(f"Entre Rios - nuevos trackers: {gps_er_created}")
    print(f"Entre Rios - ya asociados: {gps_er_existing}")
    print(f"Total GPS-ER funcionando: {gps_er_created + gps_er_existing}/15")

    print(f"\nESTADO ESPERADO:")
    print("- simple_10_cows_emulator.py -> 10 animales en Granja Norte")
    print("- start_emulator_5192.py -> 15 animales en Entre Rios - Vaca GPS")
    print("\nAhora ambos emuladores deberian funcionar simultaneamente!")

if __name__ == "__main__":
    main()