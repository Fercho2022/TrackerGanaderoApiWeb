import psycopg2

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

        print("Actualizando estados de animales...")

        # Mostrar estados actuales
        print("\nEstados actuales:")
        cursor.execute('SELECT "Id", "Name", "Status" FROM "Animals" ORDER BY "Id";')
        animals = cursor.fetchall()
        for animal in animals:
            print(f"ID {animal[0]}: {animal[1]} - {animal[2]}")

        # Actualizar algunos animales a "Sick"
        print("\nCambiando animales 3, 6, 9 a 'Sick'...")
        cursor.execute('UPDATE "Animals" SET "Status" = %s WHERE "Id" IN %s', ('Sick', (3, 6, 9)))

        # Actualizar algunos animales a "Monitoring"
        print("Cambiando animales 4, 7 a 'Monitoring'...")
        cursor.execute('UPDATE "Animals" SET "Status" = %s WHERE "Id" IN %s', ('Monitoring', (4, 7)))

        # Confirmar cambios
        conn.commit()
        print("Cambios guardados!")

        # Mostrar estados actualizados
        print("\nEstados actualizados:")
        cursor.execute('SELECT "Id", "Name", "Status" FROM "Animals" ORDER BY "Id";')
        animals = cursor.fetchall()
        for animal in animals:
            print(f"ID {animal[0]}: {animal[1]} - {animal[2]}")

        # Mostrar conteo por estado
        print("\nResumen:")
        cursor.execute('SELECT "Status", COUNT(*) FROM "Animals" GROUP BY "Status" ORDER BY "Status";')
        counts = cursor.fetchall()
        for status, count in counts:
            print(f"{status}: {count} animales")

        cursor.close()
        conn.close()
        print("\nActualizacion completada!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    update_animal_statuses()