#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar los trackers y device IDs de los animales ER001-ER010
"""

import psycopg2

def check_trackers():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host="localhost",
            database="CattleTrackingDB",
            user="postgres",
            password="Ferchitovil1830",
            port="5432"
        )

        cursor = conn.cursor()

        print("Verificando trackers y device IDs para animales ER001-ER010...")
        print("=" * 60)

        # Verificar trackers de los animales ER001-ER010
        cursor.execute('''
            SELECT
                a."Tag" as animal_tag,
                a."Name" as animal_name,
                t."Id" as tracker_id,
                t."DeviceId" as device_id
            FROM "Animals" a
            JOIN "Trackers" t ON a."TrackerId" = t."Id"
            WHERE a."Tag" IN ('ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010')
            ORDER BY a."Tag"
        ''')

        results = cursor.fetchall()

        print(f"{'Animal Tag':<10} | {'Tracker ID':<12} | {'Device ID':<20} | Animal Name")
        print("-" * 70)

        for result in results:
            animal_tag, animal_name, tracker_id, device_id = result
            print(f"{animal_tag:<10} | {tracker_id:<12} | {device_id or 'NULL':<20} | {animal_name}")

        print("\n" + "=" * 60)
        print("Emulador emulator_10_cows.py debe usar estos Device IDs:")
        for result in results:
            animal_tag, _, _, device_id = result
            if device_id:
                print(f"  {animal_tag}: {device_id}")
            else:
                print(f"  {animal_tag}: SIN DEVICE ID - PROBLEMA!")

    except psycopg2.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

    return True

if __name__ == "__main__":
    check_trackers()