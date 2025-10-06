#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mover animales ER001-ER010 a Granja Norte
Esto corregirá el filtro por granja en la aplicación
"""

import psycopg2
import sys

def fix_farm_assignments():
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

        print("Verificando estado actual de las granjas...")

        # Verificar granjas
        cursor.execute('SELECT "Id", "Name" FROM "Farms" ORDER BY "Id"')
        farms = cursor.fetchall()
        print("\nGranjas disponibles:")
        for farm in farms:
            print(f"  Farm ID {farm[0]}: {farm[1]}")

        # Verificar animales por granja ANTES
        cursor.execute('''
            SELECT
                f."Name" as farm_name,
                COUNT(a."Id") as animal_count,
                STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
            FROM "Farms" f
            LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
            GROUP BY f."Id", f."Name"
            ORDER BY f."Id"
        ''')

        results_before = cursor.fetchall()
        print("\nANTES del cambio - Animales por granja:")
        for result in results_before:
            farm_name, count, tags = result
            print(f"  {farm_name}: {count} animales ({tags or 'ninguno'})")

        # Ejecutar la actualización
        print("\nMoviendo animales ER001-ER010 a Granja Norte...")

        update_sql = '''
            UPDATE "Animals"
            SET "FarmId" = 8,
                "UpdatedAt" = NOW()
            WHERE "Tag" IN ('ER001', 'ER002', 'ER003', 'ER004', 'ER005', 'ER006', 'ER007', 'ER008', 'ER009', 'ER010')
        '''

        cursor.execute(update_sql)
        rows_affected = cursor.rowcount
        print(f"  {rows_affected} animales movidos exitosamente")

        # Verificar animales por granja DESPUÉS
        cursor.execute('''
            SELECT
                f."Name" as farm_name,
                COUNT(a."Id") as animal_count,
                STRING_AGG(a."Tag", ', ' ORDER BY a."Tag") as animal_tags
            FROM "Farms" f
            LEFT JOIN "Animals" a ON f."Id" = a."FarmId"
            GROUP BY f."Id", f."Name"
            ORDER BY f."Id"
        ''')

        results_after = cursor.fetchall()
        print("\nDESPUES del cambio - Animales por granja:")
        for result in results_after:
            farm_name, count, tags = result
            print(f"  {farm_name}: {count} animales ({tags or 'ninguno'})")

        # Confirmar cambios
        conn.commit()
        print("\nResultado esperado:")
        print("  - Entre Rios - Vaca GPS: solo GPS-ER-001")
        print("  - Granja norte: ER001, ER002, ER003, ER004, ER005, ER006, ER007, ER008, ER009, ER010")
        print("\nFiltro por granja corregido exitosamente!")

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
    print("Iniciando correccion del filtro por granja...")
    print("=" * 50)

    success = fix_farm_assignments()

    if success:
        print("\n" + "=" * 50)
        print("Correccion completada!")
        print("Ahora prueba la aplicacion:")
        print("   1. Selecciona 'Entre Rios - Vaca GPS' -> debe mostrar solo GPS-ER-001")
        print("   2. Selecciona 'Granja norte' -> debe mostrar ER001-ER010")
    else:
        print("\nLa correccion fallo. Revisa los errores arriba.")
        sys.exit(1)