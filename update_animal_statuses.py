import psycopg2
import sys

def update_animal_statuses():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host="localhost",
            database="tracker_ganadero",
            user="postgres",
            password="123456"
        )
        cursor = conn.cursor()

        print("🔄 Actualizando estados de animales...")
        print()

        # Mostrar estados actuales
        print("📋 Estados actuales:")
        cursor.execute('SELECT "Id", "Name", "Tag", "Status" FROM "Animals" ORDER BY "Id";')
        animals = cursor.fetchall()
        for animal in animals:
            print(f"ID {animal[0]}: {animal[1]} ({animal[2]}) - {animal[3]}")
        print()

        # Actualizar algunos animales a "Sick"
        print("🔴 Cambiando animales 3, 6, 9 a estado 'Sick' (Enfermo)...")
        cursor.execute('UPDATE "Animals" SET "Status" = %s WHERE "Id" IN %s', ('Sick', (3, 6, 9)))

        # Actualizar algunos animales a "Monitoring"
        print("🟡 Cambiando animales 4, 7 a estado 'Monitoring' (En observación)...")
        cursor.execute('UPDATE "Animals" SET "Status" = %s WHERE "Id" IN %s', ('Monitoring', (4, 7)))

        # Confirmar cambios
        conn.commit()
        print("✅ Cambios guardados en la base de datos!")
        print()

        # Mostrar estados actualizados
        print("📋 Estados actualizados:")
        cursor.execute('SELECT "Id", "Name", "Tag", "Status" FROM "Animals" ORDER BY "Id";')
        animals = cursor.fetchall()
        for animal in animals:
            print(f"ID {animal[0]}: {animal[1]} ({animal[2]}) - {animal[3]}")
        print()

        # Mostrar conteo por estado
        print("📊 Resumen por estado:")
        cursor.execute('SELECT "Status", COUNT(*) as "Cantidad" FROM "Animals" GROUP BY "Status" ORDER BY "Status";')
        status_counts = cursor.fetchall()
        for status_count in status_counts:
            status_spanish = {
                'Healthy': 'Saludable',
                'Sick': 'Enfermo',
                'Monitoring': 'En observación'
            }.get(status_count[0], status_count[0])
            print(f"  {status_count[0]} ({status_spanish}): {status_count[1]} animales")

        cursor.close()
        conn.close()

        print()
        print("🎉 Actualización completada exitosamente!")
        print("Ahora puedes probar el filtrado en la Gestión de animales.")

    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

    return True

if __name__ == "__main__":
    success = update_animal_statuses()
    if not success:
        sys.exit(1)