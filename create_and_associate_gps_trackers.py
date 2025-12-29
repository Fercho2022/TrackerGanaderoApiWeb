#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear los trackers faltantes para GPS-ER-011 a GPS-ER-015
y asociarlos con sus animales correspondientes
"""

import requests
import json

API_BASE_URL = "http://localhost:5192/api"

def get_animals_by_farm(farm_id):
    """Obtiene todos los animales de una granja específica"""
    try:
        response = requests.get(f"{API_BASE_URL}/Animals")
        response.raise_for_status()
        animals = response.json()
        return [animal for animal in animals if animal['farmId'] == farm_id and animal['tag'].startswith('GPS-ER-')]
    except Exception as e:
        print(f"Error obteniendo animales: {e}")
        return []

def get_tracker_by_device_id(device_id):
    """Verifica si existe un tracker con el device ID específico"""
    try:
        response = requests.get(f"{API_BASE_URL}/Trackers")
        response.raise_for_status()
        trackers = response.json()
        return next((t for t in trackers if t['deviceId'] == device_id), None)
    except Exception as e:
        print(f"Error obteniendo trackers: {e}")
        return None

def create_tracker(device_id):
    """Crea un nuevo tracker"""
    try:
        tracker_data = {
            "deviceId": device_id,
            "model": "GPS Tracker v1.0",
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

def update_animal_tracker(animal_id, tracker_id):
    """Actualiza el tracker de un animal"""
    try:
        # Obtener datos actuales del animal
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        # Crear DTO para actualización
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
        print(f"Error actualizando animal {animal_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    print("CREACION Y ASOCIACION DE TRACKERS GPS-ER FALTANTES")
    print("=" * 70)

    # Obtener animales GPS-ER de la granja 7
    animals = get_animals_by_farm(7)
    animals.sort(key=lambda x: x['tag'])

    print(f"Animales GPS-ER encontrados: {len(animals)}")

    # Procesar cada animal
    trackers_created = 0
    associations_made = 0

    for animal in animals:
        tag = animal['tag']
        animal_id = animal['id']
        current_tracker_id = animal['trackerId']

        # Extraer número del tag
        if tag.startswith('GPS-ER-'):
            try:
                tag_number = int(tag.split('-')[-1])
                expected_device_id = f"COW_GPS_ER_{tag_number:02d}"

                # Verificar si el tracker ya existe
                existing_tracker = get_tracker_by_device_id(expected_device_id)

                if existing_tracker:
                    tracker_id = existing_tracker['id']

                    if current_tracker_id != tracker_id:
                        print(f"ASOCIANDO: {tag} -> {expected_device_id} (Tracker {tracker_id})")
                        if update_animal_tracker(animal_id, tracker_id):
                            associations_made += 1
                            print(f"  OK - Asociacion completada")
                        else:
                            print(f"  ERROR - Fallo la asociacion")
                    else:
                        print(f"YA ASOCIADO: {tag} -> {expected_device_id} (Tracker {tracker_id})")

                else:
                    # El tracker no existe, crearlo
                    print(f"CREANDO TRACKER: {expected_device_id} para {tag}")
                    new_tracker = create_tracker(expected_device_id)

                    if new_tracker:
                        tracker_id = new_tracker['id']
                        trackers_created += 1
                        print(f"  OK - Tracker {tracker_id} creado")

                        # Asociar con el animal
                        print(f"ASOCIANDO: {tag} -> {expected_device_id} (Tracker {tracker_id})")
                        if update_animal_tracker(animal_id, tracker_id):
                            associations_made += 1
                            print(f"  OK - Asociacion completada")
                        else:
                            print(f"  ERROR - Fallo la asociacion")
                    else:
                        print(f"  ERROR - Fallo la creacion del tracker")

            except ValueError:
                print(f"ERROR: Tag invalido {tag}")
        else:
            print(f"IGNORADO: {tag} (no es tag GPS-ER)")

    print("\n" + "=" * 70)
    print("RESUMEN:")
    print(f"Trackers creados: {trackers_created}")
    print(f"Asociaciones realizadas: {associations_made}")
    print(f"Total animales procesados: {len(animals)}")

if __name__ == "__main__":
    main()