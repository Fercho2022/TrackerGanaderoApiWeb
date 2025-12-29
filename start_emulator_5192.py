#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPS Emulator para Entre Rios - Puerto 5192
Emula 15 vacas GPS pastando en Entre Rios, Argentina
"""

import requests
import json
import time
import random
import math
import threading
from datetime import datetime, timezone

class AnimalGPSTracker:
    def __init__(self, animal_number: int, center_lat: float, center_lng: float, api_url: str):
        # Configuracion del dispositivo - cada animal tiene su propio device_id
        self.animal_number = animal_number
        self.device_id = f"COW_GPS_ER_{animal_number:02d}"  # COW_GPS_ER_01, COW_GPS_ER_02, etc.
        self.tag = f"GPS-ER-{animal_number:03d}"  # GPS-ER-001, GPS-ER-002, etc.
        self.api_url = api_url

        # Coordenadas del centro de Entre Rios con pequeña variacion para cada animal
        self.center_lat = center_lat + random.uniform(-0.002, 0.002)  # ~200m variacion
        self.center_lng = center_lng + random.uniform(-0.002, 0.002)

        # Area de pastoreo individual (aproximadamente 500m x 500m por animal)
        self.grazing_radius = 0.005  # ~500 metros en grados

        # Estado inicial del animal (posicion aleatoria dentro de su area)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.grazing_radius * 0.5)
        self.current_lat = self.center_lat + distance * math.cos(angle)
        self.current_lng = self.center_lng + distance * math.sin(angle)

        # Estados de comportamiento individuales
        self.is_resting = random.choice([True, False])
        self.rest_cycles = 0
        self.max_rest_cycles = random.randint(2, 6)

        # Configuracion de simulacion
        self.send_interval = random.randint(15, 25)  # Intervalo variable entre animales
        self.is_active = True

    def generate_realistic_movement(self):
        """Genera movimiento realista individual para cada vaca"""
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
                self.max_rest_cycles = random.randint(2, 6)
        else:
            # Movimiento normal de pastoreo
            lat_change = random.uniform(-0.002, 0.002)  # ~200 metros
            lng_change = random.uniform(-0.002, 0.002)
            speed = random.uniform(0.2, 1.8)  # m/s realista para pastoreo
            activity = random.randint(4, 9)  # Actividad media-alta

            # Chance de empezar a descansar (diferente por animal)
            if random.random() < 0.15:  # 15% chance
                self.is_resting = True
                self.rest_cycles = 0

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
            direction_lat = (self.center_lat - self.current_lat) * 0.2
            direction_lng = (self.center_lng - self.current_lng) * 0.2
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
            "temperature": round(random.uniform(36.5, 39.5), 1),  # Temperatura corporal normal
            "batteryLevel": random.randint(75, 100),
            "signalStrength": random.randint(70, 95),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def send_data(self, data):
        """Envia datos al API"""
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 200:
                status = "Descansando" if self.is_resting else "Pastando"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.tag} - {status}")
                print(f"   Ubicacion: {data['latitude']}, {data['longitude']} | Vel: {data['speed']} m/s")
                return True
            else:
                print(f"Error HTTP {response.status_code} para {self.tag}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error conexion {self.tag}: {e}")
            return False

class EntreRiosGPSEmulator:
    def __init__(self, api_base_url: str = "http://localhost:5192"):
        self.api_url = f"{api_base_url}/api/tracking/tracker-data"

        # Coordenadas del centro de Entre Rios (Gualeguaychu)
        self.center_lat = -33.0167
        self.center_lng = -58.5167

        # Crear 15 animales GPS
        self.animals = []
        for i in range(1, 16):  # 1 a 15
            animal = AnimalGPSTracker(i, self.center_lat, self.center_lng, self.api_url)
            self.animals.append(animal)

        # Configuracion de la simulacion
        self.total_duration = 60 * 60  # 60 minutos
        self.cycle_count = 0

        print("Iniciando Emulador GPS - Entre Rios...")
        print("=" * 70)
        print("GPS EMULADOR - 15 VACAS GPS ENTRE RIOS, ARGENTINA")
        print("=" * 70)
        print("Granja: Entre Rios - Vaca GPS")
        print(f"Animales: 15 vacas GPS (GPS-ER-001 a GPS-ER-015)")
        print(f"Ubicacion: Gualeguaychu, Entre Rios ({self.center_lat}, {self.center_lng})")
        print(f"Area total: ~1.5km x 1.5km")
        print(f"Duracion: {self.total_duration // 60} minutos")
        print(f"API: {api_base_url}")
        print("=" * 70)
        for animal in self.animals:
            print(f"  {animal.tag} -> Device: {animal.device_id}")
        print("=" * 70)
        print()

    def run_animal_simulation(self, animal, stop_event):
        """Ejecuta la simulacion para un animal individual"""
        cycle_count = 0
        try:
            while not stop_event.is_set():
                cycle_count += 1

                # Generar y enviar datos del animal
                tracker_data = animal.generate_tracker_data()
                success = animal.send_data(tracker_data)

                if not success:
                    print(f"   Falló envío para {animal.tag}")

                # Esperar con intervalo individual del animal
                time.sleep(animal.send_interval)

        except Exception as e:
            print(f"Error en {animal.tag}: {e}")

        print(f"\n{animal.tag} completó {cycle_count} ciclos")

    def run(self):
        """Ejecuta el emulador para todos los animales en paralelo"""
        print("Iniciando simulación GPS para 15 vacas...")
        print("Presiona Ctrl+C para detener\n")

        start_time = time.time()
        stop_event = threading.Event()
        threads = []

        try:
            # Crear un hilo para cada animal
            for animal in self.animals:
                thread = threading.Thread(
                    target=self.run_animal_simulation,
                    args=(animal, stop_event),
                    daemon=True
                )
                thread.start()
                threads.append(thread)
                time.sleep(0.5)  # Escalonar el inicio de los animales

            print(f"Todos los animales iniciados. Simulación por {self.total_duration // 60} minutos...")

            # Esperar hasta que termine el tiempo o se interrumpa
            time.sleep(self.total_duration)

        except KeyboardInterrupt:
            print(f"\n\nEmulador detenido por el usuario después de {(time.time() - start_time):.0f} segundos")

        # Detener todos los hilos
        stop_event.set()

        # Esperar a que terminen todos los hilos
        for thread in threads:
            thread.join(timeout=5)

        print(f"\nSimulación GPS completada para las 15 vacas de Entre Rios")
        print("Datos GPS finalizados.")

if __name__ == "__main__":
    # Crear y ejecutar el emulador
    emulator = EntreRiosGPSEmulator()
    emulator.run()