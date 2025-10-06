import requests

try:
    print("Actualizando estados de animales...")
    response = requests.post("http://localhost:5192/api/debug/update-animal-statuses")

    if response.status_code == 200:
        result = response.json()
        print("¡Actualización exitosa!")
        print("\nCambios realizados:")
        for update in result.get("Updates", []):
            print(f"  - {update}")

        print(f"\nResumen de estados:")
        for status in result.get("StatusSummary", []):
            spanish_status = {
                "Healthy": "Saludable",
                "Sick": "Enfermo",
                "Monitoring": "En observación"
            }.get(status["Status"], status["Status"])
            print(f"  - {status['Status']} ({spanish_status}): {status['Count']} animales")

        print(f"\nTodos los animales:")
        for animal in result.get("AllAnimals", []):
            spanish_status = {
                "Healthy": "Saludable",
                "Sick": "Enfermo",
                "Monitoring": "En observación"
            }.get(animal["Status"], animal["Status"])
            print(f"  ID {animal['Id']}: {animal['Name']} - {animal['Status']} ({spanish_status})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
    print("\nAsegurate de que:")
    print("1. El API este ejecutandose")
    print("2. Hayas agregado el DebugController.cs al proyecto")
    print("3. Hayas recompilado el API")