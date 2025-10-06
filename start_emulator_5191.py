#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cow_gps_emulator import CowGPSEmulator

if __name__ == "__main__":
    print("Iniciando emulador GPS en puerto 5192...")
    emulator = CowGPSEmulator("http://localhost:5192")
    emulator.run_simulation(60)