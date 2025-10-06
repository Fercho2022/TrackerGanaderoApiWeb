#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPS Emulator para Entre Rios - Puerto 5192
Emula una vaca pastando en Entre Rios, Argentina
"""

import requests
import json
import time
import random
import math
from datetime import datetime

class EntreRiosGPSEmulator:
    def __init__(self, api_base_url: str = "http://localhost:5192"):
        # Configuracion del dispositivo
        self.device_id = "COW_GPS_ENTRE_RIOS"  # Matched with GPS-ER-001 animal tracker
        self.api_url = f"{api_base_url}/api/tracking/tracker-data"

        # Coordenadas del centro de Entre Rios (Gualeguaychu)
        self.center_lat = -33.0167
        self.center_lng = -58.5167

        # Area de pastoreo (aproximadamente 800m x 800m)
        self.grazing_radius = 0.007  # ~800 metros en grados

        # Estado del animal
        self.current_lat = self.center_lat
        self.current_lng = self.center_lng
        self.is_resting = False
        self.rest_cycles = 0
        self.max_rest_cycles = random.randint(2, 4)

        # Configuracion de la simulacion
        self.send_interval = 20  # segundos
        self.total_duration = 60 * 60  # 60 minutos
        self.cycle_count = 0

        print("Iniciando Emulador GPS - Entre Rios...")
        print("=" * 60)
        print("GPS EMULADOR - ENTRE RIOS, ARGENTINA")
        print("=" * 60)
        print(f"Vaca: {self.device_id}")
        print(f"Ubicacion: Gualeguaychu, Entre Rios ({self.center_lat}, {self.center_lng})")
        print(f"Area de pastoreo: ~800m x 800m")
        print(f"Frecuencia: cada {self.send_interval} segundos")
        print(f"Duracion: {self.total_duration // 60} minutos")
        print(f"API: {api_base_url}")
        print("=" * 60)
        print()

    def generate_realistic_movement(self):
        """Genera movimiento realista de una vaca pastando"""
        if self.is_resting:
            # Durante el descanso, movimiento muy limitado
            lat_change = random.uniform(-0.0001, 0.0001)  # ~10 metros
            lng_change = random.uniform(-0.0001, 0.0001)
            speed = 0.0
            activity = random.randint(1, 3)  # Baja actividad
            self.rest_cycles += 1

            if self.rest_cycles >= self.max_rest_cycles:
                self.is_resting = False
                self.rest_cycles = 0
                self.max_rest_cycles = random.randint(2, 4)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Vaca termino de descansar")
        else:
            # Movimiento normal de pastoreo
            # Cambios mas grandes pero dentro del area
            lat_change = random.uniform(-0.003, 0.003)  # ~300 metros
            lng_change = random.uniform(-0.003, 0.003)
            speed = random.uniform(0.2, 1.5)  # m/s realista para pastoreo
            activity = random.randint(4, 8)  # Actividad media-alta

            # Chance de empezar a descansar
            if random.random() < 0.2:  # 20% chance
                self.is_resting = True
                self.rest_cycles = 0
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Vaca empieza a descansar/rumiar")

        # Aplicar el movimiento pero mantener dentro del area
        new_lat = self.current_lat + lat_change
        new_lng = self.current_lng + lng_change

        # Verificar que este dentro del area de pastoreo
        distance_from_center = math.sqrt(
            (new_lat - self.center_lat) ** 2 +
            (new_lng - self.center_lng) ** 2
        )

        if distance_from_center <= self.grazing_radius:
            self.current_lat = new_lat
            self.current_lng = new_lng
        else:
            # Si se sale del area, mover hacia el centro
            direction_lat = (self.center_lat - self.current_lat) * 0.1
            direction_lng = (self.center_lng - self.current_lng) * 0.1
            self.current_lat += direction_lat
            self.current_lng += direction_lng

        return speed, activity

    def generate_tracker_data(self):
        """Genera datos completos del tracker GPS"""
        speed, activity = self.generate_realistic_movement()

        return {
            "deviceId": self.device_id,
            "latitude": round(self.current_lat, 6),
            "longitude": round(self.current_lng, 6),
            "altitude": round(random.uniform(15.0, 25.0), 1),  # Entre Rios es bastante plano
            "speed": round(speed, 1),
            "activityLevel": activity,
            "temperature": round(random.uniform(36.0, 40.0), 1),  # Temperatura corporal normal
            "batteryLevel": random.randint(85, 100),
            "signalStrength": random.randint(70, 95),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def send_data(self, data):
        """Envia datos al API"""
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                status = "Descansando" if self.is_resting else "Pastando"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] DATOS ENVIADOS - {status}")
                print(f"   Ubicacion: {data['latitude']}, {data['longitude']}")
                print(f"   Velocidad: {data['speed']} m/s | Temp: {data['temperature']}C")
                return True
            else:
                print(f"Error HTTP {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error de conexion: {e}")
            return False

    def run(self):
        """Ejecuta el emulador"""
        start_time = time.time()

        try:
            while time.time() - start_time < self.total_duration:
                self.cycle_count += 1
                print(f"\n--- CICLO {self.cycle_count} ---")

                # Generar y enviar datos
                tracker_data = self.generate_tracker_data()
                success = self.send_data(tracker_data)

                if not success:
                    print("Falló el envío de datos. Reintentando en el próximo ciclo...")

                # Esperar hasta el siguiente envío
                time.sleep(self.send_interval)

        except KeyboardInterrupt:
            print(f"\n\nEmulador detenido por el usuario después de {self.cycle_count} ciclos")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        print(f"\nEmulacion completada. Total de ciclos: {self.cycle_count}")
        print("Datos del GPS Entre Rios finalizados.")

if __name__ == "__main__":
    # Crear y ejecutar el emulador
    emulator = EntreRiosGPSEmulator()
    emulator.run()