#!/usr/bin/env python3
import serial
import csv
import time
import sys

# Configuration Parameters
SERIAL_PORT = '/dev/ttyACM0'  # Your verified Linux character device
BAUD_RATE = 115200
OUTPUT_FILE = 'wifi_3d_spatial_log.csv'

def get_simulated_3d_coordinates():
    """
    Simulates spatial inputs (Latitude, Longitude, Altitude).
    In production, you can tie this to a laptop GPS daemon, 
    an internal cellular card tracking matrix, or step increments.
    """
    # Baseline coordinates for your immediate environment
    base_lat = 32.0833
    base_lon = 34.8000
    base_alt = 30.0  # Altitude in meters (Z-axis for 3D mapping)
    
    # Adding slight drift over time to simulate a walking tracking path
    drift = time.time() % 60 / 100000
    return base_lat + drift, base_lon + drift, base_alt + (drift * 10)

print(f"[*] Initializing Serial Listener on {SERIAL_PORT}...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow port initialization buffer
    ser.flushInput()
except Exception as e:
    print(f"[-] Hardware Layer Error: Could not bind to interface {SERIAL_PORT}: {e}")
    sys.exit(1)

print(f"[*] Logging matrix initialized. Writing data captures to {OUTPUT_FILE}")

# Initialize CSV Structure
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'SSID', 'BSSID', 'RSSI_dBm', 'Channel', 'Latitude', 'Longitude', 'Altitude_m'])

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # Read line from the ESP32 UART pipe
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Filter out system header text
                if not raw_line or "STARTING" in raw_line or "DATA_FORMAT" in raw_line:
                    continue
                
                # Split the CSV payload from the chip
                data_fields = raw_line.split(',')
                if len(data_fields) == 4:
                    ssid, bssid, rssi, channel = data_fields
                    
                    # Intersect Layer 2 metrics with Layer 1 Spatial Coordinates
                    lat, lon, alt = get_simulated_3d_coordinates()
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Commit to persistent disk log
                    with open(OUTPUT_FILE, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, ssid, bssid, rssi, channel, lat, lon, alt])
                    
                    print(f"[CAPTURE] BSSID: {bssid} | RSSI: {rssi} dBm | Ch: {channel} | Z: {alt:.1f}m -> Logged")
            except Exception as parse_error:
                # Catch malformed bits from noisy serial reads
                continue
except KeyboardInterrupt:
    print("\n[*] Mapping capture suspended. Disengaging serial hooks cleanly.")
    ser.close()
