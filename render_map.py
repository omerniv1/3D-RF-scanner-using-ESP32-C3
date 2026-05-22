#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
#from max_rssi_filter import apply_radio_threshold  # Optional clean-up hook

def render_3d_wifi_cloud(csv_path):
    try:
        # Load the telemetry matrix
        df = pd.read_csv(csv_path)
        if df.empty:
            print("[-] Dataset is empty. Keep the scanner running longer to accumulate data points.")
            return
    except FileNotFoundError:
        print(f"[-] Target log matrix not found at {csv_path}. Verify your scanner script output path.")
        return

    print(f"[*] Processing {len(df)} telemetry captures...")

    # Initialize the spatial projection figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Assign coordinate matrices
    x = df['Longitude']
    y = df['Latitude']
    z = df['Altitude_m']
    colors = df['RSSI_dBm']  # Color mapping represents L1 RF amplitude

    # Generate spatial scatter matrix 
    # c=colors references the signal strength, cmap='viridis' transitions dark-to-bright
    scatter = ax.scatter(x, y, z, c=colors, cmap='viridis', marker='o', s=40, edgecolors='k', depthshade=True)

    # Decorate axes with spatial attributes
    ax.set_title('3D Radio Propagation Environment Map', fontsize=14, pad=20)
    ax.set_xlabel('Spatial Axis: Longitude', labelpad=10)
    ax.set_ylabel('Spatial Axis: Latitude', labelpad=10)
    ax.set_zlabel('Vertical Elevation: Altitude (Meters)', labelpad=10)

    # Append structural color bar legend detailing RF attenuation thresholds
    cbar = fig.colorbar(scatter, ax=ax, pad=0.1, shrink=0.6)
    cbar.set_label('Received Signal Strength Indicator (RSSI in dBm)', rotation=270, labelpad=15)

    print("[*] Launching rendering visualization loop...")
    plt.show()

if __name__ == '__main__':
    render_3d_wifi_cloud('wifi_3d_spatial_log.csv')
