#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para asociar los trackers GPS con los animales GPS-ER-001 a GPS-ER-015
en la granja "Entre Rios - Vaca GPS" (Farm ID 7)
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5192/api"

def get_animals_by_farm(farm_id):
    """Obtiene todos los animales de una granja específica"""
    try:
        response = requests.get(f"{API_BASE_URL}/Animals")
        response.raise_for_status()
        animals = response.json()

        # Filtrar solo los animales de la granja específica con tags GPS-ER
        farm_animals = [animal for animal in animals
                       if animal['farmId'] == farm_id and animal['tag'].startswith('GPS-ER-')]

        return farm_animals
    except Exception as e:
        print(f"Error obteniendo animales: {e}")
        return []

def get_all_trackers():
    """Obtiene todos los trackers del sistema"""
    try:
        response = requests.get(f"{API_BASE_URL}/Trackers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error obteniendo trackers: {e}")
        return []

def update_animal_tracker(animal_id, tracker_id):
    """Actualiza el tracker de un animal"""
    try:
        # Primero obtener los datos actuales del animal
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        # Actualizar solo el trackerId
        update_data = {
            "name": animal_data["name"],
            "tag": animal_data["tag"],
            "birthDate": animal_data["birthDate"],
            "gender": animal_data["gender"],
            "breed": animal_data["breed"],
            "weight": animal_data["weight"],
            "status": animal_data["status"],
            "trackerId": tracker_id
        }

        response = requests.put(f"{API_BASE_URL}/Animals/{animal_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error actualizando animal {animal_id} con tracker {tracker_id}: {e}")
        return False

def main():
    print("ASOCIACION DE TRACKERS GPS ENTRE RIOS")
    print("=" * 60)

    # Obtener animales de la granja 7 (Entre Rios - Vaca GPS)
    animals = get_animals_by_farm(7)
    print(f"Encontrados {len(animals)} animales GPS-ER en la granja Entre Rios - Vaca GPS")

    # Obtener todos los trackers
    trackers = get_all_trackers()
    print(f"Encontrados {len(trackers)} trackers en el sistema")

    # Crear mapeo de device IDs a tracker IDs
    device_to_tracker = {}
    for tracker in trackers:
        device_id = tracker['deviceId']
        if device_id.startswith('COW_GPS_ER_'):
            device_to_tracker[device_id] = tracker['id']

    print(f"\nTrackers COW_GPS_ER encontrados: {len(device_to_tracker)}")

    # Mapear tags de animales a device IDs esperados
    associations_made = 0
    associations_pending = 0

    print("\nPROCESANDO ASOCIACIONES:")
    print("-" * 60)

    for animal in sorted(animals, key=lambda x: x['tag']):
        tag = animal['tag']
        animal_id = animal['id']
        current_tracker = animal['trackerId']

        # Extraer número del tag (GPS-ER-001 -> 1, GPS-ER-002 -> 2, etc.)
        if tag.startswith('GPS-ER-'):
            try:
                tag_number = int(tag.split('-')[-1])
                expected_device_id = f"COW_GPS_ER_{tag_number:02d}"

                if expected_device_id in device_to_tracker:
                    tracker_id = device_to_tracker[expected_device_id]

                    if current_tracker != tracker_id:
                        print(f"ASOCIANDO: {tag} (Animal {animal_id}) -> Tracker {tracker_id} ({expected_device_id})")

                        if update_animal_tracker(animal_id, tracker_id):
                            associations_made += 1
                            print(f"  OK - Asociacion completada")
                        else:
                            print(f"  ERROR - Fallo la asociacion")
                    else:
                        print(f"YA ASOCIADO: {tag} -> Tracker {tracker_id} ({expected_device_id})")
                else:
                    print(f"PENDIENTE: {tag} -> {expected_device_id} (tracker no creado aun)")
                    associations_pending += 1

            except ValueError:
                print(f"ERROR: Tag invalido {tag}")
        else:
            print(f"IGNORADO: {tag} (no es tag GPS-ER)")

    print("\n" + "=" * 60)
    print("RESUMEN:")
    print(f"Asociaciones realizadas: {associations_made}")
    print(f"Asociaciones pendientes: {associations_pending}")
    print(f"Total animales procesados: {len(animals)}")

    if associations_pending > 0:
        print(f"\nNOTA: {associations_pending} trackers aun no han sido creados.")
        print("Esto sucede cuando el GPS emulator envia datos por primera vez.")
        print("Ejecuta este script nuevamente en unos minutos.")

if __name__ == "__main__":
    main()