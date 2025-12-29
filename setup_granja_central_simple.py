#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para configurar Granja Central usando SQL directo
"""

import psycopg2
import json

def setup_granja_central_db():
    """Configura la Granja Central directamente en la base de datos"""

    print("=" * 60)
    print("CONFIGURANDO GRANJA CENTRAL DIRECTAMENTE EN DB")
    print("=" * 60)

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="root"
        )

        cur = conn.cursor()

        print("\n1. Creando Granja Central...")

        # 1. Crear granja (si no existe)
        create_farm_sql = """
            INSERT INTO "Farms" ("Name", "Address", "UserId", "CreatedAt")
            SELECT 'Granja Central', 'Granja Central - Centro de Operaciones GPS', 1, NOW()
            WHERE NOT EXISTS (SELECT 1 FROM "Farms" WHERE "Name" = 'Granja Central');
        """

        cur.execute(create_farm_sql)
        print("✅ Granja Central creada/verificada")

        print("\n2. Creando trackers...")

        # 2. Crear trackers
        for i in range(1, 11):
            device_id = f"COW_NORTH_FARM_{i:02d}"
            tracker_name = f"Tracker Granja Central {i:02d}"

            create_tracker_sql = """
                INSERT INTO "Trackers" ("DeviceId", "Name", "Status", "FirmwareVersion", "CreatedAt")
                SELECT %s, %s, 'Active', 'v2.0', NOW()
                WHERE NOT EXISTS (SELECT 1 FROM "Trackers" WHERE "DeviceId" = %s);
            """

            cur.execute(create_tracker_sql, (device_id, tracker_name, device_id))
            print(f"✅ Tracker {device_id} creado/verificado")

        print("\n3. Creando animales...")

        # 3. Crear animales
        for i in range(1, 11):
            device_id = f"COW_NORTH_FARM_{i:02d}"
            animal_name = f"Vaca Central {i:02d}"
            tag = f"GC{i:03d}"

            breeds = ['Holstein', 'Angus', 'Brahman', 'Hereford']
            genders = ['Female', 'Male']

            breed = breeds[i % len(breeds)]
            gender = genders[i % len(genders)]
            weight = 400.0 + (i * 10)

            create_animal_sql = """
                INSERT INTO "Animals" ("Name", "Tag", "Gender", "Breed", "BirthDate", "Weight", "Status", "FarmId", "TrackerId", "CreatedAt", "UpdatedAt")
                SELECT %s, %s, %s, %s, '2021-01-01', %s, 'Active',
                       (SELECT "Id" FROM "Farms" WHERE "Name" = 'Granja Central'),
                       (SELECT "Id" FROM "Trackers" WHERE "DeviceId" = %s),
                       NOW(), NOW()
                WHERE NOT EXISTS (SELECT 1 FROM "Animals" WHERE "Tag" = %s);
            """

            cur.execute(create_animal_sql, (animal_name, tag, gender, breed, weight, device_id, tag))
            print(f"✅ Animal {tag} ({animal_name}) creado/verificado")

        # Commit todas las transacciones
        conn.commit()

        print("\n4. Verificando configuración...")

        # 4. Verificar resultados
        verify_sql = """
            SELECT
                f."Name" as farm_name,
                f."Id" as farm_id,
                COUNT(a."Id") as animal_count,
                STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
            FROM "Farms" f
            LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
            WHERE f."Name" = 'Granja Central'
            GROUP BY f."Name", f."Id";
        """

        cur.execute(verify_sql)
        result = cur.fetchone()

        if result:
            farm_name, farm_id, animal_count, animal_tags = result
            print(f"📊 Granja: {farm_name} (ID: {farm_id})")
            print(f"📊 Animales: {animal_count}")
            print(f"📊 Tags: {animal_tags}")

        # Cerrar conexión
        cur.close()
        conn.close()

        print("\n" + "=" * 60)
        print("🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("📝 Pasos siguientes:")
        print("1. El emulador ya está enviando datos (verificar logs de la API)")
        print("2. Abrir la aplicación web: http://localhost:PORT")
        print("3. Ir a 'Mapa en Tiempo Real'")
        print("4. Seleccionar 'Granja Central' en el dropdown")
        print("5. Ver los 10 animales moviéndose en el mapa")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    setup_granja_central_db()