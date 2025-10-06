#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manual para enviar datos a todas las vacas ER001-ER010
"""

import requests
import time
import random

def send_test_data_for_all_cows():
    """Envía datos de prueba para todas las vacas ER001-ER010"""

    # Base coordinates (Entre Ríos, Argentina)
    base_lat = -33.0167
    base_lng = -58.5167

    print("Enviando datos de prueba para todas las vacas ER001-ER010...")
    print("=" * 60)

    successful_sends = 0

    for i in range(1, 11):
        device_id = f"COW_GPS_ER_{i:02d}"
        tag = f"ER{i:03d}"

        # Generar posición ligeramente diferente para cada vaca
        lat_offset = random.uniform(-0.005, 0.005)  # ~500m de variación
        lng_offset = random.uniform(-0.005, 0.005)

        test_data = {
            "deviceId": device_id,
            "latitude": base_lat + lat_offset,
            "longitude": base_lng + lng_offset,
            "altitude": round(random.uniform(15.0, 30.0), 1),
            "speed": round(random.uniform(0.0, 3.0), 1),
            "activityLevel": random.randint(1, 10),
            "temperature": round(random.uniform(36.0, 40.0), 1),
            "batteryLevel": random.randint(85, 100),
            "signalStrength": random.randint(70, 95),
            "timestamp": "2025-10-03T19:00:00.000Z"
        }

        try:
            print(f"Enviando datos para {tag} ({device_id})...")
            print(f"  Posicion: {test_data['latitude']:.6f}, {test_data['longitude']:.6f}")

            response = requests.post(
                "http://localhost:5192/api/tracking/tracker-data",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                print(f"  SUCCESS: {tag} - Datos enviados exitosamente")
                successful_sends += 1
            else:
                print(f"  ERROR: {tag} - HTTP {response.status_code}: {response.text}")

        except Exception as e:
            print(f"  EXCEPTION: {tag} - {e}")

        # Pequeña pausa entre envíos
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print(f"RESUMEN: {successful_sends}/10 vacas recibieron datos exitosamente")

    if successful_sends == 10:
        print("Todos los animales ER001-ER010 deberian tener coordenadas GPS ahora!")
    else:
        print(f"{10 - successful_sends} animales fallaron")

    return successful_sends == 10

if __name__ == "__main__":
    send_test_data_for_all_cows()