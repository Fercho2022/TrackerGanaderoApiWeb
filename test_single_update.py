#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script para verificar que la API funciona con una sola actualizacion
"""

import requests
import random
from datetime import datetime, timezone

def test_single_cow_update():
    """Prueba actualizar una sola vaca para verificar que la API funciona"""

    # Datos para ER001
    device_id = "COW_GPS_ER_01"
    tag = "ER001"

    # Coordenadas base (Entre Rios, Argentina)
    base_lat = -33.0167
    base_lng = -58.5167

    # Pequeno movimiento
    lat_offset = random.uniform(-0.001, 0.001)
    lng_offset = random.uniform(-0.001, 0.001)

    current_lat = base_lat + lat_offset
    current_lng = base_lng + lng_offset

    # Datos GPS
    gps_data = {
        "deviceId": device_id,
        "latitude": round(current_lat, 6),
        "longitude": round(current_lng, 6),
        "altitude": round(random.uniform(15.0, 30.0), 1),
        "speed": round(random.uniform(0.0, 2.5), 1),
        "activityLevel": random.randint(1, 10),
        "temperature": round(random.uniform(36.5, 39.5), 1),
        "batteryLevel": random.randint(85, 100),
        "signalStrength": random.randint(75, 95),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print(f"Probando actualizar {tag} con coordenadas: {current_lat:.6f}, {current_lng:.6f}")
    print(f"Datos GPS: {gps_data}")

    try:
        response = requests.post(
            "http://localhost:5192/api/tracking/tracker-data",
            json=gps_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"Codigo de respuesta: {response.status_code}")

        if response.status_code == 200:
            print(f"EXITO: {tag} actualizado correctamente")
            return True
        else:
            print(f"ERROR: Codigo {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False

    except Exception as e:
        print(f"EXCEPCION: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== PRUEBA DE ACTUALIZACION UNICA ===")
    success = test_single_cow_update()

    if success:
        print("\nLa API funciona correctamente. Podemos proceder con el emulador completo.")
    else:
        print("\nHay problemas con la API. Revisar configuracion.")