import requests
import json

# Verificar que el API esté funcionando
base_url = "http://localhost:5192/api"

# Datos para actualizar directamente con PATCH o usando el endpoint correcto
updates = [
    # Animales Enfermos (Sick)
    {"id": 3, "status": "Sick", "name": "Vaca GPS Entre Rios"},
    {"id": 6, "status": "Sick", "name": "Vaca Entre Rios 03"},
    {"id": 9, "status": "Sick", "name": "Vaca Entre Rios 06"},

    # Animales En observación (Monitoring)
    {"id": 4, "status": "Monitoring", "name": "Vaca Entre Rios 01"},
    {"id": 7, "status": "Monitoring", "name": "Vaca Entre Rios 04"},

    # Animales Saludables (Healthy)
    {"id": 5, "status": "Healthy", "name": "Vaca Entre Rios 02"},
    {"id": 8, "status": "Healthy", "name": "Vaca Entre Rios 05"},
    {"id": 10, "status": "Healthy", "name": "Vaca Entre Rios 07"},
    {"id": 11, "status": "Healthy", "name": "Vaca Entre Rios 08"},
    {"id": 12, "status": "Healthy", "name": "Vaca Entre Rios 09"},
    {"id": 13, "status": "Healthy", "name": "Vaca Entre Rios 10"}
]

print("Actualizando estados de animales...")

for update_data in updates:
    animal_id = update_data["id"]
    new_status = update_data["status"]
    animal_name = update_data["name"]

    try:
        # Obtener animal actual
        get_response = requests.get(f"{base_url}/animals/{animal_id}")

        if get_response.status_code == 200:
            animal = get_response.json()

            # Forzar el cambio de status
            animal["status"] = new_status

            print(f"Actualizando {animal_name} (ID: {animal_id}) -> {new_status}")

            # Hacer PUT con todos los datos
            put_response = requests.put(
                f"{base_url}/animals/{animal_id}",
                json=animal,
                headers={"Content-Type": "application/json"}
            )

            if put_response.status_code in [200, 204]:
                print(f"  ✓ Actualizado exitosamente")

                # Verificar que se guardó
                verify_response = requests.get(f"{base_url}/animals/{animal_id}")
                if verify_response.status_code == 200:
                    verify_animal = verify_response.json()
                    actual_status = verify_animal.get("status", "Unknown")
                    print(f"  -> Estado verificado: {actual_status}")
                else:
                    print(f"  ! Error verificando estado")
            else:
                print(f"  ✗ Error en actualización: {put_response.status_code}")
                print(f"     Response: {put_response.text}")
        else:
            print(f"Error obteniendo animal {animal_id}: {get_response.status_code}")

    except Exception as e:
        print(f"Error con animal {animal_id}: {e}")

print("\n" + "="*50)
print("Verificación final de todos los animales:")

try:
    response = requests.get(f"{base_url}/animals")
    if response.status_code == 200:
        animals = response.json()

        status_counts = {}
        for animal in animals:
            status = animal.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

            spanish_status = {
                "Healthy": "Saludable",
                "Sick": "Enfermo",
                "Monitoring": "En observación",
                "Active": "Activo"
            }.get(status, status)

            print(f"ID {animal['id']}: {animal['name'][:25]:<25} - {status} ({spanish_status})")

        print(f"\nResumen:")
        for status, count in status_counts.items():
            spanish = {
                "Healthy": "Saludable",
                "Sick": "Enfermo",
                "Monitoring": "En observación",
                "Active": "Activo"
            }.get(status, status)
            print(f"  {status} ({spanish}): {count} animales")

except Exception as e:
    print(f"Error en verificación final: {e}")

print("\n¡Actualización completada!")
print("Reinicia la aplicación MAUI para ver los cambios.")