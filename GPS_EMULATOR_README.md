# 🐄 Emulador GPS - Tracker Ganadero

Este emulador simula una vaca pastando en Entre Ríos, Argentina, con un collar GPS que envía datos cada 20 segundos a tu API web.

## 📋 Archivos Incluidos

- `gps_emulator.py` - Emulador principal GPS
- `setup_test_cow.py` - Script para configurar datos de prueba
- `requirements.txt` - Dependencias de Python

## 🚀 Configuración e Instalación

### 1. Instalar Python y dependencias
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar la base de datos (una sola vez)
```bash
# Ejecutar la API
dotnet run

# En otra terminal, configurar datos de prueba
python setup_test_cow.py
```

Este script creará:
- ✅ Una granja en Entre Ríos, Argentina
- ✅ Una vaca llamada "Vaca Esperanza" (Tag: ER-001)
- ✅ Un tracker GPS asociado (COW_TRACKER_001)

## 🎮 Uso del Emulador

### 1. Ejecutar la API
```bash
dotnet run
```

### 2. Ejecutar el emulador GPS
```bash
python gps_emulator.py
```

### 3. Ver en el mapa
1. Abre tu app Blazor Hybrid MAUI
2. Ve a la página "Mapa en Tiempo Real"
3. Selecciona la granja "Estancia Entre Ríos - Prueba GPS"
4. ¡Verás la vaca moviéndose en tiempo real!

## 🌍 Ubicación de la Simulación

**📍 Entre Ríos, Argentina**
- Coordenadas centrales: -33.0167, -58.5167 (Gualeguaychú)
- Área de pastoreo: ~800m x 800m
- Comportamiento: Movimiento realista de pastoreo con períodos de descanso

## 🔧 Características del Emulador

### 🚶‍♀️ Movimiento Realista
- Velocidad: 0.2 - 1.5 m/s (caminata normal de vaca)
- Dirección: Cambios graduales, no movimientos erráticos
- Área limitada: No sale del área de pastoreo definida
- Períodos de descanso: 15% probabilidad de descansar por ~1 minuto

### 📊 Datos del Sensor
- **GPS**: Latitud, longitud, altitud
- **Movimiento**: Velocidad, nivel de actividad
- **Biométricos**: Temperatura corporal (36.5-39.5°C)
- **Técnicos**: Batería, señal GPS

### ⏰ Frecuencia
- Envío cada 20 segundos
- Duración configurable (default: 60 minutos)

## 🗺️ Visualización en Blazor MAUI

El mapa mostrará:
- 🟢 Marcador verde (vaca saludable)
- 📍 Ubicación actualizada cada 20 segundos
- ℹ️ Info popup con detalles:
  - Nombre del animal
  - Tag
  - Estado de salud
  - Velocidad actual
  - Última actualización

## 🛠️ Personalización

### Cambiar ubicación:
Edita en `gps_emulator.py`:
```python
self.center_lat = -31.7333  # Tu latitud
self.center_lng = -60.5333  # Tu longitud
```

### Cambiar comportamiento:
```python
self.max_speed = 1.5          # Velocidad máxima
self.rest_probability = 0.15  # Probabilidad de descanso
self.pasture_radius = 0.007   # Tamaño del área
```

### Cambiar frecuencia:
```python
time.sleep(20)  # Cambiar a otros segundos
```

## 🐛 Solución de Problemas

### ❌ Error de conexión
- Verifica que la API esté ejecutándose (`dotnet run`)
- Confirma la URL (default: http://localhost:5190)
- Revisa que el puerto esté disponible

### ❌ No aparece en el mapa
1. Verifica que el animal y tracker estén creados correctamente
2. Ejecuta `setup_test_cow.py` si no lo has hecho
3. Refresca el mapa en la app Blazor MAUI
4. Asegúrate de seleccionar la granja correcta en el filtro

### ❌ Error 400/500 de la API
- Revisa los logs de la API (`dotnet run`)
- Verifica que la base de datos PostgreSQL esté ejecutándose
- Confirma que las migraciones están aplicadas

## 🎯 Casos de Uso

1. **Demo en vivo**: Mostrar el tracking funcionando
2. **Testing**: Probar la funcionalidad de tracking
3. **Desarrollo**: Simular datos mientras desarrollas nuevas features
4. **Capacitación**: Entrenar usuarios con datos realistas

## 📈 Datos Generados

Cada 20 segundos se envía:
```json
{
  "deviceId": "COW_TRACKER_001",
  "latitude": -33.016234,
  "longitude": -58.516789,
  "altitude": 15.2,
  "speed": 0.8,
  "activityLevel": 5,
  "temperature": 38.2,
  "batteryLevel": 92,
  "signalStrength": 87,
  "timestamp": "2025-01-XX..."
}
```

---
**🎉 ¡Disfruta viendo tu vaca virtual pastando en Entre Ríos!**