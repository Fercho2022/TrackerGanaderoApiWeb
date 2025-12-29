#!/usr/bin/env python3
import requests
import time

def test_granja_central():
    print("=" * 60)
    print("VERIFICANDO CONFIGURACION DE GRANJA CENTRAL")
    print("=" * 60)

    base_url = "http://localhost:5192/api"

    # Verificar si existen granjas
    print("\n1. Verificando granjas existentes...")
    for farm_id in range(1, 15):
        try:
            response = requests.get(f"{base_url}/Tracking/farm/{farm_id}/animals", timeout=5)
            if response.status_code == 200:
                animals = response.json()
                print(f"Granja {farm_id}: {len(animals)} animales")
                if animals:
                    for animal in animals[:3]:  # Solo mostrar primeros 3
                        print(f"  - {animal.get('name', 'N/A')} ({animal.get('tag', 'N/A')})")
        except:
            continue

    print("\n" + "=" * 60)
    print("PASOS PARA CONFIGURAR MANUALMENTE:")
    print("=" * 60)
    print("1. Conectar a PostgreSQL (pgAdmin o psql)")
    print("2. Ejecutar el archivo: setup_granja_central.sql")
    print("3. Verificar que se crearon:")
    print("   - 1 granja: 'Granja Central'")
    print("   - 10 trackers: COW_NORTH_FARM_01 a COW_NORTH_FARM_10")
    print("   - 10 animales: GC001 a GC010")
    print("4. Ejecutar: python simple_10_cows_emulator.py")
    print("5. Abrir el mapa y seleccionar 'Granja Central'")
    print("=" * 60)

    # Mostrar el contenido del archivo SQL
    print("\nCONTENIDO DEL ARCHIVO SQL A EJECUTAR:")
    print("-" * 40)
    with open("setup_granja_central.sql", "r", encoding="utf-8") as f:
        print(f.read())

if __name__ == "__main__":
    test_granja_central()