# 🎯 Configuración de Granja Central - Tracker Ganadero

## 📋 Resumen
Este documento explica cómo configurar la **Granja Central** para que los trackers del archivo `simple_10_cows_emulator.py` se muestren en el mapa en tiempo real.

## 🔧 Archivos Creados
- **`granja_central_completo.sql`** - Script SQL completo para ejecutar en PostgreSQL
- **`setup_final.py`** - Script Python con instrucciones detalladas
- **`setup_granja_central.sql`** - Script SQL alternativo más detallado
- **Endpoint API**: `/api/Tracking/setup-granja-central` (mejorado en TrackingController.cs)

## 📡 Datos del Tracker Real
Los trackers ganaderos reales envían:

### Datos GPS:
- **Latitud/Longitud**: Coordenadas precisas
- **Altitud**: Altura sobre nivel del mar
- **Velocidad**: km/h del animal
- **Precisión**: Margen de error en metros

### Datos del Dispositivo:
- **Device ID**: Identificador único (COW_NORTH_FARM_01, etc.)
- **Timestamp**: Fecha/hora de la lectura
- **Batería**: Porcentaje restante
- **Señal GPS/Celular**: Calidad de conexión

### Sensores Biométricos:
- **Temperatura corporal**: °C del animal
- **Actividad**: Nivel de movimiento
- **Postura**: Estado del animal (de pie, echado, etc.)

## 🚀 Pasos de Configuración

### 1. Ejecutar SQL en PostgreSQL
```bash
# Opción 1: Usar pgAdmin
1. Abrir pgAdmin
2. Conectar a la base de datos 'postgres'
3. Abrir el archivo: granja_central_completo.sql
4. Ejecutar todo el script

# Opción 2: Usar psql (si está disponible)
psql -h localhost -p 5432 -U postgres -d postgres -f granja_central_completo.sql
```

### 2. Verificar Configuración
El script SQL incluye consultas de verificación que mostrarán:
- ✅ 1 granja: "Granja Central"
- ✅ 10 trackers: COW_NORTH_FARM_01 a COW_NORTH_FARM_10
- ✅ 10 animales: GC001 a GC010

### 3. Ejecutar Emulador
```bash
cd ProyectoApiWebTrackerGanadero
python simple_10_cows_emulator.py
```

### 4. Verificar en el Mapa
1. Abrir la aplicación web
2. Ir a **"Mapa en Tiempo Real"**
3. Seleccionar **"Granja Central"** en el dropdown
4. Ver los 10 animales moviéndose en el mapa

## 📊 Estructura de Datos Creada

### Granja
- **Nombre**: Granja Central
- **Dirección**: Centro de Operaciones GPS
- **User ID**: 1

### Trackers (10 dispositivos)
```
COW_NORTH_FARM_01 → Tracker Granja Central 01
COW_NORTH_FARM_02 → Tracker Granja Central 02
...
COW_NORTH_FARM_10 → Tracker Granja Central 10
```

### Animales (10 vacas)
```
GC001 → Vaca Central 01 (Male, Holstein, 410kg)
GC002 → Vaca Central 02 (Female, Angus, 420kg)
GC003 → Vaca Central 03 (Male, Brahman, 430kg)
...
GC010 → Vaca Central 10 (Female, Angus, 500kg)
```

## 🗺️ Ubicación en el Mapa
- **Centro**: Gualeguaychú, Entre Ríos, Argentina
- **Coordenadas**: -33.0167, -58.5167
- **Área de pastoreo**: ~500m x 500m por animal

## 🔍 Funcionalidades del Mapa
- **Filtro por granja**: Dropdown para seleccionar "Granja Central"
- **Vista en tiempo real**: Actualización automática cada 15 segundos
- **Seguimiento individual**: Click en cualquier animal para vista detallada
- **Información completa**: Hover para ver datos del tracker

## ⚠️ Solución de Problemas

### Si no aparecen animales:
1. Verificar que el SQL se ejecutó correctamente
2. Confirmar que el emulador está enviando datos
3. Revisar logs de la API en puerto 5192
4. Verificar conexión a PostgreSQL

### Si la API no está corriendo:
```bash
cd ProyectoApiWebTrackerGanadero
dotnet run
```

### Si hay errores de conexión:
- Verificar PostgreSQL en puerto 5432
- Confirmar credenciales (usuario: postgres, password: root)
- Verificar que la base de datos 'postgres' existe

## ✅ Resultado Esperado
Después de la configuración exitosa:
- **Dropdown "Granja Central"** visible en el mapa
- **10 animales GPS** moviéndose en tiempo real
- **Datos biométricos** actualizados constantemente
- **Interface intuitiva** para seguimiento individual

---
*Generado para el sistema Tracker Ganadero - Configuración de Granja Central*