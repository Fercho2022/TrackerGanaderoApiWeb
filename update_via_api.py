import requests

def update_animal_statuses():
    base_url = "http://localhost:5192/api"

    try:
        print("Actualizando estados de animales via API...")

        # Datos de animales a actualizar
        updates = [
            {"id": 3, "status": "Sick"},
            {"id": 6, "status": "Sick"},
            {"id": 9, "status": "Sick"},
            {"id": 4, "status": "Monitoring"},
            {"id": 7, "status": "Monitoring"}
        ]

        for update in updates:
            url = f"{base_url}/animals/{update['id']}"

            # Primero obtener el animal actual
            response = requests.get(url)
            if response.status_code == 200:
                animal = response.json()
                print(f"Actualizando animal ID {update['id']}: {animal.get('name', 'Unknown')} -> {update['status']}")

                # Actualizar solo el status
                animal['status'] = update['status']

                # Enviar la actualización
                put_response = requests.put(url, json=animal)
                if put_response.status_code == 200:
                    print(f"  ✓ Animal {update['id']} actualizado exitosamente")
                else:
                    print(f"  ✗ Error actualizando animal {update['id']}: {put_response.status_code}")
            else:
                print(f"  ✗ Error obteniendo animal {update['id']}: {response.status_code}")

        print("\nActualizacion completada!")
        print("Ahora puedes probar los diferentes estados en la aplicacion:")
        print("- Healthy -> Saludable (verde)")
        print("- Sick -> Enfermo (rojo)")
        print("- Monitoring -> En observacion (amarillo)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_animal_statuses()