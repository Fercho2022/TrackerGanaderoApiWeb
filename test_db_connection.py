#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script para verificar la conexion a PostgreSQL y los datos existentes
"""

import psycopg2
import sys

def test_database_connection():
    """Prueba la conexion a la base de datos y verifica los datos existentes"""

    try:
        # Configuracion de conexion
        conn = psycopg2.connect(
            host="localhost",
            database="CattleTrackingDB",
            user="postgres",
            password="postgres",
            port="5432"
        )

        cursor = conn.cursor()

        print("=== CONEXION A BASE DE DATOS EXITOSA ===")

        # Verificar trackers existentes
        cursor.execute('SELECT "Id", "DeviceId", "IsActive", "LastSignal" FROM "Trackers" ORDER BY "DeviceId"')
        trackers = cursor.fetchall()

        print(f"\n--- TRACKERS ENCONTRADOS ({len(trackers)}) ---")
        for tracker in trackers:
            print(f"ID: {tracker[0]}, DeviceId: {tracker[1]}, Activo: {tracker[2]}, Ultima senal: {tracker[3]}")

        # Verificar animales
        cursor.execute('SELECT "Id", "Tag", "Name", "TrackerId", "FarmId" FROM "Animals" ORDER BY "Tag"')
        animals = cursor.fetchall()

        print(f"\n--- ANIMALES ENCONTRADOS ({len(animals)}) ---")
        for animal in animals:
            print(f"ID: {animal[0]}, Tag: {animal[1]}, Nombre: {animal[2]}, TrackerID: {animal[3]}, FarmID: {animal[4]}")

        # Verificar ubicaciones recientes
        cursor.execute('''
            SELECT lh."AnimalId", a."Tag", lh."Latitude", lh."Longitude", lh."Timestamp"
            FROM "LocationHistories" lh
            JOIN "Animals" a ON lh."AnimalId" = a."Id"
            ORDER BY lh."Timestamp" DESC
            LIMIT 10
        ''')
        recent_locations = cursor.fetchall()

        print(f"\n--- UBICACIONES RECIENTES ({len(recent_locations)}) ---")
        for location in recent_locations:
            print(f"Animal: {location[1]} (ID: {location[0]}), Lat: {location[2]}, Lng: {location[3]}, Tiempo: {location[4]}")

        # Verificar relaciones tracker-animal
        cursor.execute('''
            SELECT t."DeviceId", a."Tag", a."Id" as AnimalId, t."Id" as TrackerId
            FROM "Trackers" t
            JOIN "Animals" a ON t."Id" = a."TrackerId"
            WHERE t."DeviceId" LIKE '%COW_GPS_ER_%'
            ORDER BY a."Tag"
        ''')
        tracker_animals = cursor.fetchall()

        print(f"\n--- RELACIONES TRACKER-ANIMAL ({len(tracker_animals)}) ---")
        for relation in tracker_animals:
            print(f"DeviceId: {relation[0]} -> Animal: {relation[1]} (AnimalID: {relation[2]}, TrackerID: {relation[3]})")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"ERROR DE CONEXION: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()

    if success:
        print("\n=== BASE DE DATOS OPERATIVA ===")
    else:
        print("\n=== PROBLEMAS CON BASE DE DATOS ===")