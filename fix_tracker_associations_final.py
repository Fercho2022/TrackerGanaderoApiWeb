#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solución final para liberar trackers y asociarlos correctamente con los animales GPS-ER
"""

import requests
import json

API_BASE_URL = "http://localhost:5192/api"

def get_all_animals():
    """Obtiene todos los animales del sistema"""
    try:
        response = requests.get(f"{API_BASE_URL}/Animals")
        response.raise_for_status()
        return response.json()
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

def liberar_tracker_de_animal(animal_id, animal_name):
    """Libera un tracker de un animal estableciendo trackerId a null"""
    try:
        # Obtener datos actuales del animal
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        # Actualizar con trackerId = null
        update_data = {
            "name": animal_data["name"],
            "tag": animal_data["tag"],
            "birthDate": animal_data["birthDate"],
            "gender": animal_data["gender"],
            "breed": animal_data["breed"],
            "weight": animal_data["weight"],
            "status": animal_data["status"],
            "farmId": animal_data["farmId"],
            "trackerId": None  # Liberar el tracker
        }

        response = requests.put(f"{API_BASE_URL}/Animals/{animal_id}",
                              json=update_data,
                              headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error liberando tracker del animal {animal_name}: {e}")
        return False

def asociar_tracker_a_animal(animal_id, tracker_id, animal_name, device_id):
    """Asocia un tracker con un animal"""
    try:
        # Obtener datos actuales del animal
        response = requests.get(f"{API_BASE_URL}/Animals/{animal_id}")
        response.raise_for_status()
        animal_data = response.json()

        # Actualizar con el nuevo trackerId
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
        print(f"Error asociando tracker {device_id} al animal {animal_name}: {e}")
        return False

def main():
    print("SOLUCION FINAL - REASIGNACION DE TRACKERS GPS-ER")
    print("=" * 60)

    # Obtener todos los animales y trackers
    animals = get_all_animals()
    trackers = get_all_trackers()

    # Filtrar animales GPS-ER de la granja 7 (Entre Rios - Vaca GPS)
    gps_er_animals = [a for a in animals if a['farmId'] == 7 and a['tag'].startswith('GPS-ER-')]
    gps_er_animals.sort(key=lambda x: x['tag'])

    # Filtrar trackers COW_GPS_ER
    gps_er_trackers = {t['deviceId']: t for t in trackers if t['deviceId'].startswith('COW_GPS_ER_')}

    # Filtrar animales de la granja 8 que tienen trackers COW_GPS_ER
    farm8_animals = [a for a in animals if a['farmId'] == 8 and a['trackerId'] is not None]

    print(f"Animales GPS-ER en granja 7: {len(gps_er_animals)}")
    print(f"Trackers COW_GPS_ER disponibles: {len(gps_er_trackers)}")
    print(f"Animales en granja 8 con trackers: {len(farm8_animals)}")

    print(f"\nPASO 1: Liberando trackers COW_GPS_ER de animales en granja 8")
    print("-" * 60)

    trackers_liberados = 0
    for animal in farm8_animals:
        if animal['trackerId']:
            # Verificar si este animal tiene un tracker COW_GPS_ER
            tracker = next((t for t in trackers if t['id'] == animal['trackerId']), None)
            if tracker and tracker['deviceId'].startswith('COW_GPS_ER_'):
                print(f"Liberando {tracker['deviceId']} del animal {animal['tag']} (granja 8)")
                if liberar_tracker_de_animal(animal['id'], animal['tag']):
                    trackers_liberados += 1
                    print(f"  ✓ Tracker liberado exitosamente")
                else:
                    print(f"  ✗ Error liberando tracker")

    print(f"\nTrackers liberados: {trackers_liberados}")

    print(f"\nPASO 2: Asociando trackers con animales GPS-ER correctos")
    print("-" * 60)

    asociaciones_exitosas = 0
    for animal in gps_er_animals:
        tag = animal['tag']
        animal_id = animal['id']

        # Extraer número del tag (GPS-ER-001 -> 1, GPS-ER-002 -> 2, etc.)
        if tag.startswith('GPS-ER-'):
            try:
                tag_number = int(tag.split('-')[-1])
                expected_device_id = f"COW_GPS_ER_{tag_number:02d}"

                if expected_device_id in gps_er_trackers:
                    tracker = gps_er_trackers[expected_device_id]
                    tracker_id = tracker['id']
                    current_tracker = animal['trackerId']

                    if current_tracker != tracker_id:
                        print(f"Asociando {tag} -> {expected_device_id} (Tracker {tracker_id})")
                        if asociar_tracker_a_animal(animal_id, tracker_id, tag, expected_device_id):
                            asociaciones_exitosas += 1
                            print(f"  ✓ Asociación exitosa")
                        else:
                            print(f"  ✗ Error en asociación")
                    else:
                        print(f"✓ YA ASOCIADO: {tag} -> {expected_device_id}")
                        asociaciones_exitosas += 1
                else:
                    print(f"⚠ TRACKER NO ENCONTRADO: {expected_device_id} para {tag}")

            except ValueError:
                print(f"✗ ERROR: Tag inválido {tag}")

    print(f"\n" + "=" * 60)
    print("RESUMEN FINAL:")
    print(f"Trackers liberados de granja 8: {trackers_liberados}")
    print(f"Asociaciones exitosas: {asociaciones_exitosas}")
    print(f"Total animales GPS-ER: {len(gps_er_animals)}")

    if asociaciones_exitosas >= 10:
        print(f"\n🎉 ¡ÉXITO! Ahora deberías ver {asociaciones_exitosas} animales en el Mapa en Vivo")
        print("Recarga la aplicación Blazor MAUI y selecciona la granja 'Entre Rios - Vaca GPS'")
    else:
        print(f"\n⚠ Algunas asociaciones fallaron. Verifica los logs arriba.")

if __name__ == "__main__":
    main()