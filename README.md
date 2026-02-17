# bpad proto1 core

Arduino core for the **bpad proto1 board** (ESP32-S3, 4MB flash, OPI PSRAM, 240×240 touchscreen).

Based on [ESP32 Arduino Core v2.0.17](https://github.com/espressif/arduino-esp32/releases/tag/2.0.17). Installs as a separate package alongside existing ESP32 cores — no conflicts.

## Quick Install (Arduino IDE)

1. Open **File → Preferences**
2. Add this URL to **Additional Board Manager URLs**:
   ```
   https://raw.githubusercontent.com/robonxt/bpad_proto1_core/main/package_bpad_proto1_index.json
   ```
3. Open **Tools → Board → Boards Manager**
4. Search for **"bpad proto1"** and install it
5. Select **Tools → Board → bpad proto1 (ESP32 v2.0.17) → bpad proto1**

## Board Settings

| Setting | Default |
|---|---|
| Flash Size | 4MB |
| PSRAM | OPI (Enabled) |
| Partition Scheme | Huge APP (3MB No OTA/1MB SPIFFS) |
| USB CDC On Boot | Enabled |
| USB Mode | Hardware CDC and JTAG |
| CPU Frequency | 240MHz |
| Upload Speed | 921600 |

> **NOTE:** If flashing fails, set **Erase All Flash Before Sketch Upload → Enabled** and use bootloader mode (hold BOOT + press RESET).

## Development Setup

If you want to build a release zip yourself:

```bash
# 1. Clone this repo
git clone https://github.com/robonxt/bpad_proto1_core.git
cd bpad_proto1_core

# 2. Download ESP32 v2.0.17 and apply customizations
python setup.py

# 3. Build release zip
python build.py
```

The build script will output the checksum and instructions for updating `package_bpad_proto1_index.json`.

## Proto1 Board Specs

- **MCU:** ESP32-S3
- **Flash:** 4MB
- **PSRAM:** OPI
- **Display:** 240×240 Touchscreen
- **Features:** 4 haptics, speaker, compass
- **ESP-IDF:** v4.4.7 (via ESP32 Arduino Core v2.0.17)

## Credits

- [Espressif Arduino ESP32 Core](https://github.com/espressif/arduino-esp32) (v2.0.17)
- [bpad hardware defs](https://github.com/b-pad/bpad_hardware_defs_for_arduino_ide)
