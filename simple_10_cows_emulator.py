#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emulador GPS simplificado para 10 vacas ER001-ER010
Emula movimiento realista en Granja Norte
"""

import requests
import time
import random
import math
from datetime import datetime, timezone

class Simple10CowsEmulator:
    def __init__(self):
        # Configuración del API
        self.api_url = "http://localhost:5192/api/tracking/tracker-data"

        # Ubicación base: Entre Ríos, Argentina (misma zona que GPS-ER-001)
        self.base_lat = -33.0167
        self.base_lng = -58.5167

        # Radio de movimiento (~1km)
        self.movement_radius = 0.009  # aprox 1km en grados

        # Inicializar vacas
        self.cows = []
        for i in range(1, 11):
            # Distribuir las vacas en un círculo alrededor del punto base
            angle = (i - 1) * (360 / 10)  # distribución uniforme
            radius = random.uniform(0.002, 0.008)  # distancia variable del centro

            # Calcular offset de posición inicial
            lat_offset = radius * math.cos(math.radians(angle))
            lng_offset = radius * math.sin(math.radians(angle))

            cow = {
                'device_id': f"COW_GPS_ER_{i:02d}",
                'name': f"Vaca Entre Rios {i:02d}",
                'tag': f"ER{i:03d}",
                'current_lat': self.base_lat + lat_offset,
                'current_lng': self.base_lng + lng_offset,
                'speed': random.uniform(0.0, 2.0),
                'activity': random.randint(1, 10),
                'temperature': random.uniform(36.0, 40.0),
                'battery': random.randint(85, 100)
            }
            self.cows.append(cow)

        print("=" * 60)
        print("EMULADOR GPS - 10 VACAS GRANJA NORTE")
        print("=" * 60)
        print(f"Ubicacion base: {self.base_lat}, {self.base_lng}")
        print(f"Animales: ER001 - ER010")
        print(f"Device IDs: COW_GPS_ER_01 - COW_GPS_ER_10")
        print(f"Actualizacion: cada 20 segundos")
        print("=" * 60)

    def update_cow_position(self, cow):
        """Actualiza la posición de una vaca con movimiento realista"""
        # Movimiento pequeño y aleatorio
        max_movement = 0.0002  # ~20 metros por ciclo

        lat_change = random.uniform(-max_movement, max_movement)
        lng_change = random.uniform(-max_movement, max_movement)

        new_lat = cow['current_lat'] + lat_change
        new_lng = cow['current_lng'] + lng_change

        # Mantener dentro del área permitida
        distance_from_center = math.sqrt(
            (new_lat - self.base_lat) ** 2 +
            (new_lng - self.base_lng) ** 2
        )

        if distance_from_center <= self.movement_radius:
            cow['current_lat'] = new_lat
            cow['current_lng'] = new_lng
        else:
            # Si se aleja mucho, mover hacia el centro
            direction_lat = (self.base_lat - cow['current_lat']) * 0.1
            direction_lng = (self.base_lng - cow['current_lng']) * 0.1
            cow['current_lat'] += direction_lat
            cow['current_lng'] += direction_lng

        # Actualizar otros valores
        cow['speed'] = random.uniform(0.0, 3.0)
        cow['activity'] = random.randint(1, 10)
        cow['temperature'] = random.uniform(36.0, 40.0)
        cow['battery'] = max(10, cow['battery'] - random.choice([0, 0, 1]))

    def send_cow_data(self, cow):
        """Envía datos GPS de una vaca al API"""
        try:
            data = {
                "deviceId": cow['device_id'],
                "latitude": round(cow['current_lat'], 6),
                "longitude": round(cow['current_lng'], 6),
                "altitude": round(random.uniform(15.0, 30.0), 1),
                "speed": round(cow['speed'], 1),
                "activityLevel": cow['activity'],
                "temperature": round(cow['temperature'], 1),
                "batteryLevel": cow['battery'],
                "signalStrength": random.randint(70, 95),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                print(f"OK   {cow['tag']} ({cow['device_id']}) - Lat: {cow['current_lat']:.6f}, Lng: {cow['current_lng']:.6f}")
                return True
            else:
                print(f"ERROR {cow['tag']} - HTTP {response.status_code}: {response.text}")
                return False

        except Exception as e:
            print(f"ERROR {cow['tag']} - Exception: {str(e)}")
            return False

    def run(self):
        """Ejecuta el emulador"""
        iteration = 0

        try:
            while True:
                iteration += 1
                print(f"\n--- ITERACION {iteration} - {datetime.now().strftime('%H:%M:%S')} ---")

                successful_sends = 0

                # Procesar cada vaca
                for cow in self.cows:
                    # Actualizar posición
                    self.update_cow_position(cow)

                    # Enviar datos
                    if self.send_cow_data(cow):
                        successful_sends += 1

                    # Pequeña pausa entre vacas
                    time.sleep(0.5)

                print(f"\nResumen: {successful_sends}/{len(self.cows)} vacas enviaron datos exitosamente")
                print("Proxima actualizacion en 20 segundos...")

                # Esperar 20 segundos
                time.sleep(15)  # 15 + (10 * 0.5) = ~20 segundos total

        except KeyboardInterrupt:
            print(f"\n\nEmulador detenido por el usuario despues de {iteration} iteraciones")
            print("Datos GPS finalizados.")
        except Exception as e:
            print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    emulator = Simple10CowsEmulator()
    emulator.run()