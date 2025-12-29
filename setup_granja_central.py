#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar Granja Central con trackers y animales
"""

import requests
import time
import json

def setup_granja_central():
    """Configura la Granja Central con todos sus datos"""

    base_url = "http://localhost:5192/api"

    print("=" * 60)
    print("CONFIGURANDO GRANJA CENTRAL")
    print("=" * 60)

    try:
        # 1. Crear la granja "Granja Central"
        print("\n1. Creando Granja Central...")
        farm_data = {
            "name": "Granja Central",
            "address": "Granja Central - Centro de Operaciones GPS",
            "userId": 1
        }

        # Crear la granja usando el endpoint de farms (si existe)
        # Si no existe, usaremos SQL raw

        # 2. Configurar trackers y animales usando endpoint personalizado
        print("\n2. Configurando trackers y animales...")
        setup_url = f"{base_url}/Tracking/setup-granja-central"

        response = requests.post(setup_url, json={}, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print("✅ Granja Central configurada exitosamente!")
            print(f"📊 Detalles: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Error configurando Granja Central: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error durante la configuración: {str(e)}")
        return False

    print("\n" + "=" * 60)
    print("CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("🎯 Pasos siguientes:")
    print("1. Ejecutar: python simple_10_cows_emulator.py")
    print("2. Abrir la aplicación web y ir a 'Mapa en Tiempo Real'")
    print("3. Seleccionar 'Granja Central' en el dropdown")
    print("4. Ver los 10 animales en el mapa")
    print("=" * 60)

    return True

if __name__ == "__main__":
    setup_granja_central()