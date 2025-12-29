#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir la asociación de trackers con animales
mediante consultas SQL directas
"""

import psycopg2
import json

# Configuracion de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'TrackerGanado',
    'user': 'postgres',
    'password': 'admin123'
}

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def show_current_state():
    """Muestra el estado actual de animales y trackers"""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()

        print("Estado actual de animales en granja 7:")
        print("=" * 60)
        cur.execute("""
            SELECT "Id", "Name", "Tag", "TrackerId"
            FROM "Animals"
            WHERE "FarmId" = 7
            ORDER BY "Tag"
        """)
        animals = cur.fetchall()

        for animal in animals:
            print(f"Animal {animal[0]}: {animal[2]} ({animal[1]}) -> Tracker: {animal[3]}")

        print("\nTrackers disponibles:")
        print("=" * 60)
        cur.execute("""
            SELECT "Id", "DeviceId", "Model", "IsActive"
            FROM "Trackers"
            ORDER BY "DeviceId"
        """)
        trackers = cur.fetchall()

        for tracker in trackers:
            print(f"Tracker {tracker[0]}: {tracker[1]} ({tracker[2]}) -> Activo: {tracker[3]}")

    except Exception as e:
        print(f"Error consultando datos: {e}")
    finally:
        cur.close()
        conn.close()

def fix_associations():
    """Corrige las asociaciones de trackers con animales"""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()

        # Mapeo de device IDs a tags de animales
        device_to_tag = {}
        for i in range(1, 16):
            device_id = f"COW_GPS_ER_{i:02d}"
            tag = f"GPS-ER-{i:03d}"
            device_to_tag[device_id] = tag

        print("Asociando trackers con animales...")
        print("=" * 60)

        associations_made = 0

        for device_id, animal_tag in device_to_tag.items():
            try:
                # Buscar el tracker por device ID
                cur.execute("""
                    SELECT "Id" FROM "Trackers" WHERE "DeviceId" = %s
                """, (device_id,))

                tracker_result = cur.fetchone()

                if tracker_result:
                    tracker_id = tracker_result[0]

                    # Buscar el animal por tag
                    cur.execute("""
                        SELECT "Id" FROM "Animals"
                        WHERE "Tag" = %s AND "FarmId" = 7
                    """, (animal_tag,))

                    animal_result = cur.fetchone()

                    if animal_result:
                        animal_id = animal_result[0]

                        # Asociar tracker con animal
                        cur.execute("""
                            UPDATE "Animals"
                            SET "TrackerId" = %s
                            WHERE "Id" = %s
                        """, (tracker_id, animal_id))

                        print(f"ASOCIADO: {animal_tag} -> Tracker {tracker_id} ({device_id})")
                        associations_made += 1
                    else:
                        print(f"Animal {animal_tag} no encontrado")
                else:
                    print(f"Tracker {device_id} no encontrado")

            except Exception as e:
                print(f"Error asociando {device_id} -> {animal_tag}: {e}")

        # Confirmar cambios
        conn.commit()
        print(f"\nAsociaciones realizadas: {associations_made}")

    except Exception as e:
        print(f"Error en el proceso: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def main():
    print("Estado ANTES de la corrección:")
    show_current_state()

    print("\n" + "=" * 60)
    print("CORRIGIENDO ASOCIACIONES...")
    print("=" * 60)

    fix_associations()

    print("\n" + "=" * 60)
    print("Estado DESPUÉS de la corrección:")
    show_current_state()

if __name__ == "__main__":
    main()