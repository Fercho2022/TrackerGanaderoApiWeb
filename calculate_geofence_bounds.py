#!/usr/bin/env python3
"""
Calculadora de límites de geofencing para el emulador GPS
Calcula los puntos exactos donde se mueve la vaca simulada
"""

import math

class GeofenceBoundsCalculator:
    def __init__(self):
        # Coordenadas del centro (igual que en gps_emulator.py)
        self.center_lat = -33.0167  # Gualeguaychú, Entre Ríos
        self.center_lng = -58.5167
        self.pasture_radius = 0.007  # ~800 metros en grados

    def calculate_bounds(self):
        """Calcula los límites exactos del área de pastoreo"""

        # Límites del rectángulo que contiene el área circular
        north = self.center_lat + self.pasture_radius
        south = self.center_lat - self.pasture_radius
        east = self.center_lng + self.pasture_radius
        west = self.center_lng - self.pasture_radius

        return {
            'center': {
                'lat': self.center_lat,
                'lng': self.center_lng
            },
            'bounds': {
                'north': north,
                'south': south,
                'east': east,
                'west': west
            },
            'corners': {
                'northeast': {'lat': north, 'lng': east},
                'northwest': {'lat': north, 'lng': west},
                'southeast': {'lat': south, 'lng': east},
                'southwest': {'lat': south, 'lng': west}
            }
        }

    def calculate_distance_meters(self, lat1, lng1, lat2, lng2):
        """Calcula distancia en metros entre dos puntos GPS"""
        R = 6371000  # Radio de la Tierra en metros

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)

        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) * math.sin(delta_lng / 2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def generate_geofence_code_csharp(self, bounds):
        """Genera código C# para configurar el geofencing en Blazor MAUI"""

        code = f"""
// Configuración de Geofencing para el emulador GPS
// Entre Ríos, Argentina - Área de pastoreo

public class EntreRiosGeofence
{{
    // Centro del área de pastoreo
    public static readonly double CenterLatitude = {bounds['center']['lat']};
    public static readonly double CenterLongitude = {bounds['center']['lng']};

    // Límites del área rectangular
    public static readonly double NorthBound = {bounds['bounds']['north']:.6f};
    public static readonly double SouthBound = {bounds['bounds']['south']:.6f};
    public static readonly double EastBound = {bounds['bounds']['east']:.6f};
    public static readonly double WestBound = {bounds['bounds']['west']:.6f};

    // Esquinas del área (para polígonos)
    public static readonly List<LatLng> PastureArea = new List<LatLng>
    {{
        new LatLng({bounds['corners']['northwest']['lat']:.6f}, {bounds['corners']['northwest']['lng']:.6f}), // Noroeste
        new LatLng({bounds['corners']['northeast']['lat']:.6f}, {bounds['corners']['northeast']['lng']:.6f}), // Noreste
        new LatLng({bounds['corners']['southeast']['lat']:.6f}, {bounds['corners']['southeast']['lng']:.6f}), // Sureste
        new LatLng({bounds['corners']['southwest']['lat']:.6f}, {bounds['corners']['southwest']['lng']:.6f})  // Suroeste
    }};

    // Radio del área circular (en metros)
    public static readonly double PastureRadiusMeters = 800;

    // Método para verificar si un punto está dentro del área
    public static bool IsWithinPastureArea(double lat, double lng)
    {{
        var distance = CalculateDistance(CenterLatitude, CenterLongitude, lat, lng);
        return distance <= PastureRadiusMeters;
    }}

    // Método para verificar si está dentro del rectángulo
    public static bool IsWithinBounds(double lat, double lng)
    {{
        return lat >= SouthBound && lat <= NorthBound &&
               lng >= WestBound && lng <= EastBound;
    }}

    private static double CalculateDistance(double lat1, double lng1, double lat2, double lng2)
    {{
        const double R = 6371000; // Radio de la Tierra en metros

        var lat1Rad = lat1 * Math.PI / 180;
        var lat2Rad = lat2 * Math.PI / 180;
        var deltaLat = (lat2 - lat1) * Math.PI / 180;
        var deltaLng = (lng2 - lng1) * Math.PI / 180;

        var a = Math.Sin(deltaLat / 2) * Math.Sin(deltaLat / 2) +
                Math.Cos(lat1Rad) * Math.Cos(lat2Rad) *
                Math.Sin(deltaLng / 2) * Math.Sin(deltaLng / 2);

        var c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));

        return R * c;
    }}
}}
"""
        return code

    def generate_map_center_javascript(self, bounds):
        """Genera código JavaScript para centrar el mapa"""

        code = f"""
// JavaScript para centrar el mapa en el área de Entre Ríos
// Añadir al LiveMap.razor

// Cambiar el centro por defecto:
const entreRiosCenter = {{ lat: {bounds['center']['lat']}, lng: {bounds['center']['lng']} }};

// Configurar el mapa para mostrar toda el área:
const mapBounds = {{
    north: {bounds['bounds']['north']:.6f},
    south: {bounds['bounds']['south']:.6f},
    east: {bounds['bounds']['east']:.6f},
    west: {bounds['bounds']['west']:.6f}
}};

// Inicializar mapa centrado en Entre Ríos:
map = new google.maps.Map(mapElement, {{
    zoom: 15,                    // Zoom apropiado para ver el área
    center: entreRiosCenter,     // Centrado en el área de pastoreo
    mapTypeId: 'hybrid',         // Vista híbrida para ver terreno
    bounds: mapBounds           // Límites del área
}});

// Opcional: Dibujar el área de geofencing
const geofenceCircle = new google.maps.Circle({{
    strokeColor: '#00FF00',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#00FF00',
    fillOpacity: 0.2,
    map: map,
    center: entreRiosCenter,
    radius: 800  // 800 metros de radio
}});
"""
        return code

    def print_detailed_info(self):
        """Imprime información detallada para configurar el geofencing"""

        bounds = self.calculate_bounds()

        print("🗺️ CONFIGURACIÓN DE GEOFENCING - ENTRE RÍOS")
        print("=" * 60)

        print(f"\n📍 CENTRO DEL ÁREA DE PASTOREO:")
        print(f"   Latitud:  {bounds['center']['lat']}")
        print(f"   Longitud: {bounds['center']['lng']}")
        print(f"   Ubicación: Gualeguaychú, Entre Ríos, Argentina")

        print(f"\n📐 LÍMITES DEL ÁREA (Rectángulo):")
        print(f"   Norte:  {bounds['bounds']['north']:.6f}")
        print(f"   Sur:    {bounds['bounds']['south']:.6f}")
        print(f"   Este:   {bounds['bounds']['east']:.6f}")
        print(f"   Oeste:  {bounds['bounds']['west']:.6f}")

        print(f"\n🔲 ESQUINAS DEL ÁREA:")
        print(f"   Noroeste: {bounds['corners']['northwest']['lat']:.6f}, {bounds['corners']['northwest']['lng']:.6f}")
        print(f"   Noreste:  {bounds['corners']['northeast']['lat']:.6f}, {bounds['corners']['northeast']['lng']:.6f}")
        print(f"   Sureste:  {bounds['corners']['southeast']['lat']:.6f}, {bounds['corners']['southeast']['lng']:.6f}")
        print(f"   Suroeste: {bounds['corners']['southwest']['lat']:.6f}, {bounds['corners']['southwest']['lng']:.6f}")

        # Calcular dimensiones del área
        width_meters = self.calculate_distance_meters(
            bounds['center']['lat'], bounds['bounds']['west'],
            bounds['center']['lat'], bounds['bounds']['east']
        )
        height_meters = self.calculate_distance_meters(
            bounds['bounds']['south'], bounds['center']['lng'],
            bounds['bounds']['north'], bounds['center']['lng']
        )

        print(f"\n📏 DIMENSIONES DEL ÁREA:")
        print(f"   Ancho:  ~{width_meters:.0f} metros")
        print(f"   Alto:   ~{height_meters:.0f} metros")
        print(f"   Radio circular: ~800 metros")

        print(f"\n🎯 PARA CONFIGURAR EN BLAZOR MAUI:")
        print(f"   1. Centrar mapa en: {bounds['center']['lat']}, {bounds['center']['lng']}")
        print(f"   2. Zoom recomendado: 15-16")
        print(f"   3. Tipo de mapa: 'hybrid' (para ver terreno)")

        print(f"\n⚠️  ALERTAS DE GEOFENCING:")
        print(f"   - Si la vaca sale del área: lat < {bounds['bounds']['south']:.6f} o lat > {bounds['bounds']['north']:.6f}")
        print(f"   - Si la vaca sale del área: lng < {bounds['bounds']['west']:.6f} o lng > {bounds['bounds']['east']:.6f}")

        return bounds

def main():
    calculator = GeofenceBoundsCalculator()
    bounds = calculator.print_detailed_info()

    print(f"\n📋 ¿Quieres generar código para Blazor MAUI? (y/n): ", end="")
    generate_code = input().strip().lower()

    if generate_code == 'y':
        print("\n" + "="*60)
        print("📝 CÓDIGO C# PARA GEOFENCING:")
        print("="*60)
        print(calculator.generate_geofence_code_csharp(bounds))

        print("\n" + "="*60)
        print("📝 CÓDIGO JAVASCRIPT PARA MAPA:")
        print("="*60)
        print(calculator.generate_map_center_javascript(bounds))

if __name__ == "__main__":
    main()