#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear datos de tracking iniciales para los 15 animales GPS
Esto forzará al sistema a crear los trackers automáticamente
"""

import requests
import json
from datetime import datetime

# Configuracion
API_URL = "http://localhost:5192/api/tracking/tracker-data"
CENTER_LAT = -33.0167
CENTER_LNG = -58.5167

def send_initial_data():
    """Envía datos iniciales para cada uno de los 15 device IDs"""

    print("Enviando datos iniciales para crear trackers automáticamente...")
    print("=" * 60)

    for i in range(1, 16):  # 1 a 15
        device_id = f"COW_GPS_ER_{i:02d}"
        tag = f"GPS-ER-{i:03d}"

        # Datos de tracking iniciales
        data = {
            "deviceId": device_id,
            "latitude": CENTER_LAT + (i * 0.001),  # Separar ligeramente cada animal
            "longitude": CENTER_LNG + (i * 0.001),
            "altitude": 20.0,
            "speed": 0.0,
            "activityLevel": 1,
            "temperature": 37.5,
            "batteryLevel": 100,
            "signalStrength": 95,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        try:
            response = requests.post(
                API_URL,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 200:
                print(f"OK {tag} ({device_id}) - Datos enviados correctamente")
            else:
                print(f"ERROR {tag} ({device_id}) - Error HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"ERROR {tag} ({device_id}) - Error de conexion: {e}")

    print("=" * 60)
    print("Datos iniciales enviados. Los trackers deberían crearse automáticamente.")

if __name__ == "__main__":
    send_initial_data()