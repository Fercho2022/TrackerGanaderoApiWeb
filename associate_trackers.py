#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para asociar automáticamente trackers con animales basado en los tags
"""

import requests
import json

# Configuracion
API_BASE = "http://localhost:5192/api"

def get_animals():
    """Obtiene todos los animales de la granja 7"""
    try:
        response = requests.get(f"{API_BASE}/farms/7/animals")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error obteniendo animales: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error de conexion: {e}")
        return []

def associate_trackers():
    """Asocia trackers con animales basado en la correspondencia de device IDs"""

    # Mapeo de tags de animales a device IDs
    tag_to_device = {}
    for i in range(1, 16):
        tag = f"GPS-ER-{i:03d}"
        device_id = f"COW_GPS_ER_{i:02d}"
        tag_to_device[tag] = device_id

    print("Obteniendo lista de animales...")
    animals = get_animals()

    if not animals:
        print("No se encontraron animales o error al conectar.")
        return

    print(f"Encontrados {len(animals)} animales en la granja 'Entre Rios - Vaca GPS'")
    print("=" * 60)

    # Para cada animal sin tracker, intentar asociarlo con un tracker
    for animal in animals:
        if animal['trackerId'] is None:
            animal_tag = animal['tag']
            animal_id = animal['id']
            animal_name = animal['name']

            if animal_tag in tag_to_device:
                device_id = tag_to_device[animal_tag]

                # Primero, enviar datos de tracking para crear el tracker si no existe
                data = {
                    "deviceId": device_id,
                    "latitude": -33.0167 + (animal_id * 0.001),
                    "longitude": -58.5167 + (animal_id * 0.001),
                    "altitude": 20.0,
                    "speed": 0.0,
                    "activityLevel": 1,
                    "temperature": 37.5,
                    "batteryLevel": 100,
                    "signalStrength": 95,
                    "timestamp": "2025-10-30T18:00:00Z"
                }

                try:
                    # Enviar datos de tracking
                    track_response = requests.post(
                        f"{API_BASE}/tracking/tracker-data",
                        json=data,
                        headers={"Content-Type": "application/json"},
                        timeout=5
                    )

                    if track_response.status_code == 200:
                        print(f"DATOS ENVIADOS: {animal_tag} -> {device_id}")
                    else:
                        print(f"ERROR enviando datos: {animal_tag} -> {device_id} (HTTP {track_response.status_code})")

                except Exception as e:
                    print(f"ERROR con {animal_tag}: {e}")
            else:
                print(f"NO ENCONTRADO mapeo para {animal_tag}")
        else:
            print(f"YA ASOCIADO: {animal['tag']} -> Tracker {animal['trackerId']}")

    print("=" * 60)
    print("Proceso completado. Verificando resultados...")

    # Verificar resultados
    updated_animals = get_animals()
    associated_count = sum(1 for animal in updated_animals if animal['trackerId'] is not None)

    print(f"Animales con tracker asociado: {associated_count} de {len(updated_animals)}")

if __name__ == "__main__":
    associate_trackers()