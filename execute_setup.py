#!/usr/bin/env python3
import os
import requests
import time

# Configuración de SQL usando requests al endpoint de la API
def execute_sql_via_api(sql_commands):
    """Ejecuta comandos SQL via endpoint de API"""
    base_url = "http://localhost:5192"

    for i, cmd in enumerate(sql_commands, 1):
        print(f"Ejecutando comando {i}...")
        print(f"SQL: {cmd[:100]}...")

        # Aquí podríamos usar un endpoint personalizado si existiera
        # Por ahora mostraremos los comandos
        print(f"✓ Comando {i} preparado")

def setup_granja_central_manual():
    """Configura Granja Central usando comandos individuales"""
    print("=" * 60)
    print("CONFIGURANDO GRANJA CENTRAL")
    print("=" * 60)

    # 1. Primero verificamos conexión a la API
    try:
        response = requests.get("http://localhost:5192/api/Tracking/farm/1/animals", timeout=5)
        if response.status_code != 200:
            print("❌ Error: API no está respondiendo correctamente")
            return False
        print("✅ API está funcionando")
    except Exception as e:
        print(f"❌ Error conectando a API: {e}")
        return False

    # 2. Crear los comandos SQL
    sql_commands = [
        # Crear granja
        """INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
        SELECT 'Granja Central', 'Granja Central - Centro de Operaciones GPS', 1, NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Farms" WHERE "Name" = 'Granja Central');""",

        # Crear trackers individualmente
        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_01', 'Tracker Granja Central 01', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_01');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_02', 'Tracker Granja Central 02', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_02');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_03', 'Tracker Granja Central 03', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_03');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_04', 'Tracker Granja Central 04', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_04');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_05', 'Tracker Granja Central 05', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_05');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_06', 'Tracker Granja Central 06', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_06');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_07', 'Tracker Granja Central 07', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_07');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_08', 'Tracker Granja Central 08', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_08');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_09', 'Tracker Granja Central 09', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_09');""",

        """INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
        SELECT 'COW_NORTH_FARM_10', 'Tracker Granja Central 10', 'Active', 'v2.0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = 'COW_NORTH_FARM_10');""",
    ]

    # Comandos para crear animales
    animal_commands = []
    for i in range(1, 11):
        device_id = f"COW_NORTH_FARM_{i:02d}"
        animal_name = f"Vaca Central {i:02d}"
        tag = f"GC{i:03d}"
        gender = "Female" if i % 2 == 0 else "Male"
        breeds = ['Holstein', 'Angus', 'Brahman', 'Hereford']
        breed = breeds[i % 4]
        weight = 400.0 + (i * 10)

        animal_sql = f"""INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
        SELECT '{animal_name}', '{tag}', '{gender}', '{breed}', '2021-01-01', {weight}, 'Active',
               (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
               (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = '{device_id}'),
               NOW(), NOW()
        WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = '{tag}');"""

        animal_commands.append(animal_sql)

    sql_commands.extend(animal_commands)

    print(f"Preparados {len(sql_commands)} comandos SQL")
    print("\n📋 INSTRUCCIONES PARA EJECUTAR MANUALMENTE:")
    print("=" * 60)
    print("1. Abrir pgAdmin o cualquier cliente PostgreSQL")
    print("2. Conectar a la base de datos 'postgres'")
    print("3. Ejecutar los siguientes comandos uno por uno:")
    print("=" * 60)

    for i, cmd in enumerate(sql_commands, 1):
        print(f"\n-- Comando {i}")
        print(cmd)

    print("\n" + "=" * 60)
    print("4. Verificar resultados con:")
    print("""
SELECT f."Name", COUNT(a."Id") as animals
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
WHERE f."Name" = 'Granja Central'
GROUP BY f."Name";
    """)

    print("5. Si todo está correcto, reiniciar el emulador:")
    print("   python simple_10_cows_emulator.py")

    print("6. Abrir el mapa y seleccionar 'Granja Central'")
    print("=" * 60)

    return True

if __name__ == "__main__":
    setup_granja_central_manual()