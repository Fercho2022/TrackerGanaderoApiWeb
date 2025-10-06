#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar coordenadas de las 10 vacas cada minuto
Solución de respaldo para mantener datos actualizados
"""

import requests
import time
import random
import math
from datetime import datetime, timezone

def update_all_cows_coordinates():
    """Actualiza las coordenadas de todas las vacas ER001-ER010"""

    # Base coordinates (Entre Ríos, Argentina)
    base_lat = -33.0167
    base_lng = -58.5167

    print(f"\n--- ACTUALIZANDO COORDENADAS - {datetime.now().strftime('%H:%M:%S')} ---")

    successful_updates = 0

    for i in range(1, 11):
        device_id = f"COW_GPS_ER_{i:02d}"
        tag = f"ER{i:03d}"

        # Generar pequeños cambios en la posición (movimiento realista)
        lat_offset = random.uniform(-0.002, 0.002)  # ~200m de variación
        lng_offset = random.uniform(-0.002, 0.002)

        # Asegurar que no se alejen demasiado del centro
        current_lat = base_lat + lat_offset
        current_lng = base_lng + lng_offset

        # Datos GPS actualizados
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

        try:
            response = requests.post(
                "http://localhost:5192/api/tracking/tracker-data",
                json=gps_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                print(f"  OK {tag}: {current_lat:.6f}, {current_lng:.6f}")
                successful_updates += 1
            else:
                print(f"  ERROR {tag}: Error {response.status_code}")

        except Exception as e:
            print(f"  ERROR {tag}: Exception - {str(e)}")

        # Pequeña pausa entre cada vaca
        time.sleep(0.5)

    print(f"\nResultado: {successful_updates}/10 vacas actualizadas")
    return successful_updates

def run_continuous_updates():
    """Ejecuta actualizaciones continuas cada 60 segundos"""
    iteration = 0

    try:
        while True:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"ITERACION {iteration} - ACTUALIZACION DE COORDENADAS GPS")
            print(f"{'='*60}")

            successful = update_all_cows_coordinates()

            if successful == 10:
                print(f"\nPERFECTO: Todas las 10 vacas actualizadas correctamente")
            elif successful > 5:
                print(f"\nPARCIAL: {successful}/10 vacas actualizadas (algunas fallaron)")
            else:
                print(f"\nPROBLEMA: Solo {successful}/10 vacas actualizadas")

            print(f"\nEsperando 60 segundos para la próxima actualización...")
            print("-" * 60)

            # Esperar 60 segundos
            time.sleep(60)

    except KeyboardInterrupt:
        print(f"\n\nActualizaciones detenidas por el usuario")
        print(f"Total de iteraciones completadas: {iteration}")

if __name__ == "__main__":
    print("INICIANDO ACTUALIZADOR DE COORDENADAS GPS")
    print("Actualiza las 10 vacas ER001-ER010 cada 60 segundos")
    print("Ubicacion: Entre Rios, Argentina")
    print("Presiona Ctrl+C para detener")

    run_continuous_updates()