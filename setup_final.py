#!/usr/bin/env python3
"""
Script final para configurar Granja Central usando conexion directa
"""
import os
import subprocess
import sys

def run_sql_command(sql_command):
    """Ejecuta un comando SQL via psql"""
    try:
        # Usar variables de entorno para la conexión
        cmd = [
            "psql",
            "-h", "localhost",
            "-p", "5432",
            "-U", "postgres",
            "-d", "postgres",
            "-c", sql_command
        ]

        # Configurar variable de entorno para contraseña
        env = os.environ.copy()
        env['PGPASSWORD'] = 'root'

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def show_manual_steps():
    """Muestra los pasos manuales para configurar"""
    print("=" * 80)
    print("CONFIGURACION MANUAL DE GRANJA CENTRAL")
    print("=" * 80)
    print("Como no se puede conectar automaticamente a PostgreSQL,")
    print("ejecuta estos comandos manualmente en pgAdmin o psql:")
    print()

    steps = [
        # Paso 1: Crear granja
        ("1. CREAR GRANJA", """
INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
SELECT 'Granja Central', 'Granja Central - Centro de Operaciones GPS', 1, NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Farms" WHERE "Name" = 'Granja Central');
"""),

        # Paso 2: Crear trackers
        ("2. CREAR TRACKERS", "")
    ]

    for title, sql in steps:
        print(f"\n{title}:")
        print("-" * 40)
        print(sql.strip())

    # Trackers individuales
    print("\n2. CREAR TRACKERS:")
    print("-" * 40)
    for i in range(1, 11):
        device_id = f"COW_NORTH_FARM_{i:02d}"
        tracker_name = f"Tracker Granja Central {i:02d}"
        print(f"""
INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
SELECT '{device_id}', '{tracker_name}', 'Active', 'v2.0', NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = '{device_id}');""")

    # Animales individuales
    print("\n3. CREAR ANIMALES:")
    print("-" * 40)
    breeds = ["Holstein", "Angus", "Brahman", "Hereford"]
    for i in range(1, 11):
        device_id = f"COW_NORTH_FARM_{i:02d}"
        animal_name = f"Vaca Central {i:02d}"
        tag = f"GC{i:03d}"
        gender = "Female" if i % 2 == 0 else "Male"
        breed = breeds[(i-1) % len(breeds)]
        weight = 400.0 + (i * 10)

        print(f"""
INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
SELECT '{animal_name}', '{tag}', '{gender}', '{breed}', '2021-01-01', {weight}, 'Active',
       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = '{device_id}'),
       NOW(), NOW()
WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = '{tag}');""")

    # Verificación
    print("\n4. VERIFICAR CONFIGURACION:")
    print("-" * 40)
    print("""
SELECT
    f."Name" as farm_name,
    f."Id" as farm_id,
    COUNT(a."Id") as animal_count,
    STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
FROM "Farms" f
LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
WHERE f."Name" = 'Granja Central'
GROUP BY f."Name", f."Id";
""")

    print("\n5. PASOS FINALES:")
    print("-" * 40)
    print("Después de ejecutar los comandos SQL:")
    print("1. Verificar que se crearon 10 animales")
    print("2. Reiniciar: python simple_10_cows_emulator.py")
    print("3. Abrir la aplicación web")
    print("4. Ir a 'Mapa en Tiempo Real'")
    print("5. Seleccionar 'Granja Central' en el dropdown")
    print("6. Ver los 10 animales moviéndose en el mapa")
    print("=" * 80)

if __name__ == "__main__":
    show_manual_steps()