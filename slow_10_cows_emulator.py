#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emulador GPS lento para 10 vacas ER001-ER010
Envía datos con intervalos más largos para evitar problemas de concurrencia
"""

import requests
import time
import random
import math
from datetime import datetime, timezone

class Slow10CowsEmulator:
    def __init__(self):
        # Configuración del API
        self.api_url = "http://localhost:5192/api/tracking/tracker-data"

        # Ubicación base: Entre Ríos, Argentina
        self.base_lat = -33.0167
        self.base_lng = -58.5167

        # Radio de movimiento (~500m para ser más conservador)
        self.movement_radius = 0.005  # ~500m en grados

        # Inicializar vacas
        self.cows = []
        for i in range(1, 11):
            # Distribuir las vacas en un círculo alrededor del punto base
            angle = (i - 1) * (360 / 10)  # distribución uniforme
            radius = random.uniform(0.001, 0.004)  # distancia más pequeña del centro

            # Calcular offset de posición inicial
            lat_offset = radius * math.cos(math.radians(angle))
            lng_offset = radius * math.sin(math.radians(angle))

            cow = {
                'device_id': f"COW_GPS_ER_{i:02d}",
                'name': f"Vaca Entre Rios {i:02d}",
                'tag': f"ER{i:03d}",
                'current_lat': self.base_lat + lat_offset,
                'current_lng': self.base_lng + lng_offset,
                'speed': random.uniform(0.0, 1.5),
                'activity': random.randint(1, 8),
                'temperature': random.uniform(36.5, 39.5),
                'battery': random.randint(85, 100)
            }
            self.cows.append(cow)

        print("=" * 60)
        print("EMULADOR GPS LENTO - 10 VACAS GRANJA NORTE")
        print("=" * 60)
        print(f"Ubicacion base: {self.base_lat}, {self.base_lng}")
        print(f"Animales: ER001 - ER010")
        print(f"Device IDs: COW_GPS_ER_01 - COW_GPS_ER_10")
        print(f"Actualizacion: cada 60 segundos (lento para evitar errores)")
        print(f"Pausa entre animales: 3 segundos")
        print("=" * 60)

    def update_cow_position(self, cow):
        """Actualiza la posición de una vaca con movimiento muy lento"""
        # Movimiento muy pequeño y aleatorio
        max_movement = 0.0001  # ~10 metros por ciclo

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
            direction_lat = (self.base_lat - cow['current_lat']) * 0.05
            direction_lng = (self.base_lng - cow['current_lng']) * 0.05
            cow['current_lat'] += direction_lat
            cow['current_lng'] += direction_lng

        # Actualizar otros valores muy gradualmente
        cow['speed'] = max(0, cow['speed'] + random.uniform(-0.2, 0.2))
        cow['speed'] = min(2.0, cow['speed'])  # Limitar velocidad máxima

        cow['activity'] = max(1, min(10, cow['activity'] + random.choice([-1, 0, 0, 1])))
        cow['temperature'] = max(36.0, min(40.0, cow['temperature'] + random.uniform(-0.1, 0.1)))
        cow['battery'] = max(10, cow['battery'] - random.choice([0, 0, 0, 0, 1]))

    def send_cow_data(self, cow):
        """Envía datos GPS de una vaca al API con manejo de errores mejorado"""
        try:
            data = {
                "deviceId": cow['device_id'],
                "latitude": round(cow['current_lat'], 6),
                "longitude": round(cow['current_lng'], 6),
                "altitude": round(random.uniform(15.0, 25.0), 1),
                "speed": round(cow['speed'], 1),
                "activityLevel": cow['activity'],
                "temperature": round(cow['temperature'], 1),
                "batteryLevel": cow['battery'],
                "signalStrength": random.randint(75, 95),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            print(f"Enviando {cow['tag']} ({cow['device_id']})...")
            print(f"  Posicion: {cow['current_lat']:.6f}, {cow['current_lng']:.6f}")

            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )

            if response.status_code == 200:
                print(f"  SUCCESS: {cow['tag']} - Datos enviados correctamente")
                return True
            else:
                print(f"  ERROR: {cow['tag']} - HTTP {response.status_code}")
                print(f"  Response: {response.text}")
                return False

        except requests.exceptions.Timeout:
            print(f"  TIMEOUT: {cow['tag']} - El servidor no respondió a tiempo")
            return False
        except requests.exceptions.ConnectionError:
            print(f"  CONNECTION ERROR: {cow['tag']} - No se pudo conectar al servidor")
            return False
        except Exception as e:
            print(f"  EXCEPTION: {cow['tag']} - {str(e)}")
            return False

    def run(self):
        """Ejecuta el emulador con intervalos largos"""
        iteration = 0

        try:
            while True:
                iteration += 1
                print(f"\n--- ITERACION {iteration} - {datetime.now().strftime('%H:%M:%S')} ---")

                successful_sends = 0

                # Procesar cada vaca CON PAUSA LARGA entre cada una
                for i, cow in enumerate(self.cows):
                    print(f"\nProcesando vaca {i+1}/10:")

                    # Actualizar posición
                    self.update_cow_position(cow)

                    # Enviar datos
                    if self.send_cow_data(cow):
                        successful_sends += 1

                    # PAUSA LARGA entre vacas (3 segundos) para evitar problemas de concurrencia
                    if i < len(self.cows) - 1:  # No pausar después de la última vaca
                        print(f"  Esperando 3 segundos antes de la siguiente vaca...")
                        time.sleep(3)

                print(f"\n{'='*50}")
                print(f"RESUMEN ITERACION {iteration}:")
                print(f"  Exitosos: {successful_sends}/{len(self.cows)} vacas")
                print(f"  Fallidos: {len(self.cows) - successful_sends}")

                if successful_sends == len(self.cows):
                    print(f"  PERFECTO: Todas las vacas enviaron datos correctamente!")
                elif successful_sends > 0:
                    print(f"  PARCIAL: Solo {successful_sends} vacas enviaron datos")
                else:
                    print(f"  PROBLEMA: Ninguna vaca pudo enviar datos")

                print(f"\nProxima actualizacion en 60 segundos...")
                print("=" * 50)

                # Esperar 60 segundos hasta la próxima iteración
                time.sleep(60)

        except KeyboardInterrupt:
            print(f"\n\nEmulador detenido por el usuario despues de {iteration} iteraciones")
            print("Datos GPS finalizados.")
        except Exception as e:
            print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    emulator = Slow10CowsEmulator()
    emulator.run()