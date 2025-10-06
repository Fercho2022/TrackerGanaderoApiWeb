import requests

base_url = "http://localhost:5192/api"

# Actualizar animal 3 a Sick
try:
    response = requests.get(f"{base_url}/animals/3")
    if response.status_code == 200:
        animal = response.json()
        animal['status'] = 'Sick'
        put_response = requests.put(f"{base_url}/animals/3", json=animal)
        print(f"Animal 3: {put_response.status_code}")
except Exception as e:
    print(f"Error animal 3: {e}")

# Actualizar animal 6 a Sick
try:
    response = requests.get(f"{base_url}/animals/6")
    if response.status_code == 200:
        animal = response.json()
        animal['status'] = 'Sick'
        put_response = requests.put(f"{base_url}/animals/6", json=animal)
        print(f"Animal 6: {put_response.status_code}")
except Exception as e:
    print(f"Error animal 6: {e}")

# Actualizar animal 9 a Sick
try:
    response = requests.get(f"{base_url}/animals/9")
    if response.status_code == 200:
        animal = response.json()
        animal['status'] = 'Sick'
        put_response = requests.put(f"{base_url}/animals/9", json=animal)
        print(f"Animal 9: {put_response.status_code}")
except Exception as e:
    print(f"Error animal 9: {e}")

# Actualizar animal 4 a Monitoring
try:
    response = requests.get(f"{base_url}/animals/4")
    if response.status_code == 200:
        animal = response.json()
        animal['status'] = 'Monitoring'
        put_response = requests.put(f"{base_url}/animals/4", json=animal)
        print(f"Animal 4: {put_response.status_code}")
except Exception as e:
    print(f"Error animal 4: {e}")

# Actualizar animal 7 a Monitoring
try:
    response = requests.get(f"{base_url}/animals/7")
    if response.status_code == 200:
        animal = response.json()
        animal['status'] = 'Monitoring'
        put_response = requests.put(f"{base_url}/animals/7", json=animal)
        print(f"Animal 7: {put_response.status_code}")
except Exception as e:
    print(f"Error animal 7: {e}")

print("Actualizacion completada!")
print("Estados actualizados:")
print("- Animales 3, 6, 9: Sick (Enfermo)")
print("- Animales 4, 7: Monitoring (En observacion)")
print("- Los demas: Healthy (Saludable)")