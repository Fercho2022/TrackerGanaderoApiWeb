#!/usr/bin/env python3
"""
Emulador GPS para Entre Rios - Tracker Ganadero
Simula vaca GPS-ER-001 pastando en Entre Rios, Argentina
Envia datos GPS cada 20 segundos a la API web
"""

import requests
import time
import random
import json
import math
from datetime import datetime, timezone
from typing import Tuple

class EntreRiosGPSEmulator:
    def __init__(self, api_base_url: str = "http://localhost:5192"):
        self.api_base_url = api_base_url
        self.device_id = "COW_GPS_ENTRE_RIOS"  # Nuevo deviceId

        # Coordenadas de Entre Rios, Argentina
        # Gualeguaychu - coordenadas exactas de la granja creada
        self.center_lat = -33.0167
        self.center_lng = -58.5167

        # Area de pastoreo realista (800m x 800m)
        self.pasture_radius = 0.007  # ~800 metros en grados

        # Estado actual de la vaca
        self.current_lat = self.center_lat
        self.current_lng = self.center_lng
        self.current_heading = random.uniform(0, 360)
        self.is_resting = False
        self.rest_time = 0

        # Parametros de comportamiento
        self.max_speed = 1.5  # m/s velocidad maxima
        self.rest_probability = 0.15  # 15% probabilidad de descansar
        self.rest_duration = 3  # ciclos de descanso

    def generate_realistic_movement(self) -> Tuple[float, float]:
        """Genera movimiento realista de pastoreo"""

        if self.is_resting:
            self.rest_time -= 1
            if self.rest_time <= 0:
                self.is_resting = False
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Vaca termino de descansar")

            # Movimiento minimo mientras descansa
            movement_distance = random.uniform(0.00001, 0.00005)
            angle_change = random.uniform(-30, 30)
        else:
            # Decide si va a empezar a descansar
            if random.random() < self.rest_probability:
                self.is_resting = True
                self.rest_time = self.rest_duration
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Vaca empieza a descansar/rumiar")
                return self.current_lat, self.current_lng

            # Movimiento normal de pastoreo
            movement_distance = random.uniform(0.0001, 0.0003)  # 10-30 metros
            angle_change = random.uniform(-45, 45)

        # Cambiar direccion gradualmente
        self.current_heading += angle_change
        self.current_heading = self.current_heading % 360

        # Calcular nueva posicion
        heading_rad = math.radians(self.current_heading)
        lat_delta = movement_distance * math.cos(heading_rad)
        lng_delta = movement_distance * math.sin(heading_rad) / math.cos(math.radians(self.current_lat))

        new_lat = self.current_lat + lat_delta
        new_lng = self.current_lng + lng_delta

        # Verificar que no salga del area de pastoreo
        distance_from_center = math.sqrt(
            (new_lat - self.center_lat) ** 2 + (new_lng - self.center_lng) ** 2
        )

        if distance_from_center > self.pasture_radius:
            # Si se sale del area, cambiar direccion hacia el centro
            self.current_heading = math.degrees(math.atan2(
                self.center_lng - self.current_lng,
                self.center_lat - self.current_lat
            )) + random.uniform(-30, 30)

            # Recalcular con nueva direccion
            heading_rad = math.radians(self.current_heading)
            lat_delta = movement_distance * 0.5 * math.cos(heading_rad)
            lng_delta = movement_distance * 0.5 * math.sin(heading_rad) / math.cos(math.radians(self.current_lat))

            new_lat = self.current_lat + lat_delta
            new_lng = self.current_lng + lng_delta

        self.current_lat = new_lat
        self.current_lng = new_lng

        return self.current_lat, self.current_lng

    def generate_tracker_data(self) -> dict:
        """Genera datos completos del tracker GPS"""

        # Obtener nueva posicion
        lat, lng = self.generate_realistic_movement()

        # Calcular velocidad basada en movimiento
        speed = 0.0 if self.is_resting else random.uniform(0.2, self.max_speed)

        # Simular otros sensores del collar
        data = {
            "deviceId": self.device_id,
            "latitude": lat,
            "longitude": lng,
            "altitude": random.uniform(10, 25),  # Entre Rios es plano
            "speed": speed,
            "activityLevel": 1 if self.is_resting else random.randint(3, 7),
            "temperature": random.uniform(36.5, 39.5),  # Temperatura corporal normal
            "batteryLevel": random.randint(85, 100),
            "signalStrength": random.randint(75, 95),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        return data

    def send_data_to_api(self, data: dict) -> bool:
        """Envia datos a la API web"""
        try:
            url = f"{self.api_base_url}/api/tracking/tracker-data"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(url, json=data, headers=headers, timeout=10)

            if response.status_code == 200:
                status = "Descansando" if self.is_resting else "Pastando"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] DATOS ENVIADOS - {status}")
                print(f"   Ubicacion: {data['latitude']:.6f}, {data['longitude']:.6f}")
                print(f"   Velocidad: {data['speed']:.1f} m/s | Temp: {data['temperature']:.1f}C")
                return True
            else:
                print(f"ERROR al enviar datos: {response.status_code} - {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"ERROR de conexion: {e}")
            return False

    def run_simulation(self, duration_minutes: int = 60):
        """Ejecuta la simulacion por el tiempo especificado"""
        print("="*60)
        print("GPS EMULADOR - ENTRE RIOS, ARGENTINA")
        print("="*60)
        print(f"Vaca: GPS-ER-001 (Vaca GPS Entre Rios)")
        print(f"Ubicacion: Gualeguaychu, Entre Rios ({self.center_lat}, {self.center_lng})")
        print(f"Area de pastoreo: ~800m x 800m")
        print(f"Frecuencia: cada 20 segundos")
        print(f"Duracion: {duration_minutes} minutos")
        print(f"API: {self.api_base_url}")
        print("="*60)

        end_time = time.time() + (duration_minutes * 60)
        cycle_count = 0

        try:
            while time.time() < end_time:
                cycle_count += 1
                print(f"\n--- CICLO {cycle_count} ---")

                # Generar y enviar datos
                tracker_data = self.generate_tracker_data()
                success = self.send_data_to_api(tracker_data)

                if not success:
                    print("Reintentando en 20 segundos...")

                # Esperar 20 segundos
                time.sleep(20)

        except KeyboardInterrupt:
            print(f"\n\nSimulacion detenida por el usuario")

        print(f"\n{'='*60}")
        print(f"SIMULACION COMPLETADA")
        print(f"Ciclos ejecutados: {cycle_count}")
        print(f"Tiempo total: {(time.time() - (end_time - duration_minutes * 60))/60:.1f} minutos")
        print(f"{'='*60}")

if __name__ == "__main__":
    print("Iniciando Emulador GPS - Entre Rios...")
    emulator = EntreRiosGPSEmulator("http://localhost:5192")
    emulator.run_simulation(60)  # 60 minutos por defecto