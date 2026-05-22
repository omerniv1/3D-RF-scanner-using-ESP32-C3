# 3D RF Spatial Analysis Scanner

A distributed, full-stack network engineering project that pairs an **ESP32-C3 edge sensor** with a **Fedora Linux host engine** to intercept, parse, and visualize 802.11 Layer 2 wireless propagation matrices inside an interactive 3D point-cloud environment.

---

## System Architecture & Data Plane

The system uses a **Distributed Host-Client Model** designed to eliminate hardware footprint complexity while optimizing data throughput:
* **The Client (ESP32-C3):** Operates at Layer 1/2. It continuously scans the 2.4GHz spectrum, strips out frame overhead, and extracts the **BSSID** (physical MAC address of the AP interface) and **RSSI** (Received Signal Strength Indicator) directly from the preamble.
* **The Host (Fedora Linux):** Binds to the kernel's native USB-CDC character device, streams raw telemetry data over UART, injects manual 3D spatial variables, and commits the records into a persistent analytics database.

---

## Repositories, Libraries & Dependencies

### Hardware Core & Embedded Toolchain
* **arduino-esp32 Core (Espressif Systems):** `https://github.com/espressif/arduino-esp32`
    * *Board Manager Index Used:* `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json`
* **esptool.py (Bootloader Utility):** `https://github.com/espressif/esptool`

### Host Operating System & Sandbox Utilities
* **Arduino IDE (Flatpak App Deployment):** `https://flathub.org/apps/cc.arduino.arduinoide`
* **PySerial (Python Serial Protocol Bridge):** `https://github.com/pyserial/pyserial`

### Data Science & Rendering Frameworks
* **Pandas (Data Alignment Matrix):** `https://github.com/pandas-dev/pandas`
* **Matplotlib (3D Engine Projection):** `https://github.com/matplotlib/matplotlib`

---

## 🔧 Installation & Host Preparation

### 1. Fedora Serial Interface Permissions
By default, Linux restricts access to raw character devices. Grant your user group permissions and punch a hole through the Flatpak sandbox environment:

```bash
# Add local user to dialout group
sudo usermod -aG dialout $USER

# Override Flatpak sandbox restrictions for the Arduino IDE
flatpak override --user --device=all cc.arduino.arduinoide
