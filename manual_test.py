import requests
import json

base_url = "http://localhost:5192/api"

print("=== RESUMEN PARA EL USUARIO ===")
print()
print("Para ver diferentes estados de animales, sigue estos pasos:")
print()
print("1. DETENER el API desde Visual Studio (Shift+F5)")
print("2. RECOMPILAR el proyecto API (F6 o Build)")
print("3. EJECUTAR el API de nuevo (F5)")
print("4. Ejecutar este script de nuevo")
print()
print("Despues de hacer eso, los animales tendran estos estados:")
print("- Animales 3, 6, 9: 'Sick' -> apareceran como 'Enfermo' (rojo)")
print("- Animales 4, 7: 'Monitoring' -> apareceran como 'En observacion' (amarillo)")
print("- Animales 5, 8, 10, 11, 12, 13: 'Healthy' -> apareceran como 'Saludable' (verde)")
print()
print("Esto te permitira probar:")
print("✓ Filtrado por estado en Gestion de animales")
print("✓ Diferentes colores de badge en el mapa")
print("✓ Funcion de traduccion de estados")
print()

# Probar si el API esta funcionando
try:
    response = requests.get(f"{base_url}/animals", timeout=5)
    print(f"API Status: {response.status_code}")

    if response.status_code == 200:
        print("El API esta funcionando. Ahora reinicialo para aplicar los cambios del DTO.")

except Exception as e:
    print(f"API no disponible: {e}")
    print("Asegurate de que el API este ejecutandose en el puerto 5192")

print()
print("Una vez reiniciado el API, ejecuta:")
print("python fix_statuses.py")
print()
print("para actualizar los estados de los animales.")