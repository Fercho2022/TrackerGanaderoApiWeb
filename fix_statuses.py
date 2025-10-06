import requests
import json

base_url = "http://localhost:5192/api"

def update_animal_status(animal_id, new_status):
    try:
        # Obtener el animal actual
        response = requests.get(f"{base_url}/animals/{animal_id}")
        if response.status_code == 200:
            animal = response.json()
            print(f"Actualizando animal {animal_id}: {animal.get('name')} -> {new_status}")

            # Actualizar el status
            animal['status'] = new_status

            # Enviar la actualización
            put_response = requests.put(f"{base_url}/animals/{animal_id}", json=animal)
            print(f"  Resultado: {put_response.status_code}")
            if put_response.status_code not in [200, 204]:
                print(f"  Error: {put_response.text}")
            return put_response.status_code in [200, 204]
        else:
            print(f"Error obteniendo animal {animal_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error con animal {animal_id}: {e}")
        return False

# Primero cambiar todos a "Healthy"
print("=== Estableciendo estado base 'Healthy' ===")
for animal_id in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
    update_animal_status(animal_id, "Healthy")

print("\n=== Cambiando algunos a 'Sick' ===")
# Cambiar algunos a "Sick" (Enfermo)
for animal_id in [3, 6, 9]:
    update_animal_status(animal_id, "Sick")

print("\n=== Cambiando algunos a 'Monitoring' ===")
# Cambiar algunos a "Monitoring" (En observación)
for animal_id in [4, 7]:
    update_animal_status(animal_id, "Monitoring")

print("\n=== Verificando estados finales ===")
try:
    response = requests.get(f"{base_url}/animals")
    if response.status_code == 200:
        animals = response.json()
        status_count = {}
        for animal in animals:
            status = animal.get('status', 'Unknown')
            status_count[status] = status_count.get(status, 0) + 1
            print(f"ID {animal['id']}: {animal['name']} - {status}")

        print(f"\nResumen de estados:")
        for status, count in status_count.items():
            spanish_status = {
                'Healthy': 'Saludable',
                'Sick': 'Enfermo',
                'Monitoring': 'En observación'
            }.get(status, status)
            print(f"  {status} ({spanish_status}): {count} animales")
    else:
        print("Error obteniendo lista de animales")
except Exception as e:
    print(f"Error verificando estados: {e}")

print("\nActualización completada!")