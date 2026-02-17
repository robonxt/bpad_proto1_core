#!/usr/bin/env python3
"""
Setup script for bpad_proto1_core.
Downloads ESP32 Arduino Core v2.0.17, extracts it, and applies proto1 customizations.

Usage:
    python setup.py
"""

import os
import sys
import shutil
import urllib.request
import zipfile

ESP32_VERSION = "2.0.17"
ESP32_ZIP_URL = f"https://github.com/espressif/arduino-esp32/releases/download/{ESP32_VERSION}/esp32-{ESP32_VERSION}.zip"
ESP32_ZIP_FILE = f"esp32-{ESP32_VERSION}.zip"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ESP32_DIR = os.path.join(SCRIPT_DIR, "esp32")

# Files we track in git (don't overwrite these)
CUSTOM_FILES = [
    os.path.join("esp32", "boards.txt"),
    os.path.join("esp32", "variants", "bpad_proto1"),
]


def download_file(url, dest):
    """Download a file with progress reporting."""
    print(f"Downloading {url}...")
    print(f"  -> {dest}")

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 / total_size)
            mb_down = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            sys.stdout.write(f"\r  Progress: {pct:.1f}% ({mb_down:.1f}/{mb_total:.1f} MB)")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, dest, reporthook=reporthook)
    print("\n  Download complete!")


def main():
    print("=" * 60)
    print("bpad proto1 core - Setup Script")
    print(f"Based on ESP32 Arduino Core v{ESP32_VERSION}")
    print("=" * 60)
    print()

    zip_path = os.path.join(SCRIPT_DIR, ESP32_ZIP_FILE)

    # Step 1: Download ESP32 core if not already present
    if not os.path.exists(zip_path):
        download_file(ESP32_ZIP_URL, zip_path)
    else:
        print(f"Found existing {ESP32_ZIP_FILE}, skipping download.")

    # Step 2: Backup our custom files
    print("\nBacking up custom files...")
    backup_dir = os.path.join(SCRIPT_DIR, "_backup")
    os.makedirs(backup_dir, exist_ok=True)

    for custom in CUSTOM_FILES:
        src = os.path.join(SCRIPT_DIR, custom)
        if os.path.exists(src):
            dst = os.path.join(backup_dir, custom)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"  Backed up: {custom}")

    # Step 3: Extract ESP32 core
    print(f"\nExtracting {ESP32_ZIP_FILE}...")
    # The zip contains esp32-{version}/ at the root
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Get the top-level directory name in the zip
        top_dirs = set()
        for name in zf.namelist():
            top = name.split('/')[0]
            top_dirs.add(top)

        print(f"  Zip contains top-level: {top_dirs}")

        # Extract to a temp directory
        temp_extract = os.path.join(SCRIPT_DIR, "_temp_extract")
        if os.path.exists(temp_extract):
            shutil.rmtree(temp_extract)
        zf.extractall(temp_extract)

    # Step 4: Move extracted files into esp32/
    print("\nMoving extracted files into esp32/ directory...")
    # The zip extracts to esp32-2.0.17/ - we need to move contents to esp32/
    extracted_dir = None
    for d in os.listdir(temp_extract):
        candidate = os.path.join(temp_extract, d)
        if os.path.isdir(candidate):
            extracted_dir = candidate
            break

    if extracted_dir is None:
        print("ERROR: Could not find extracted directory!")
        sys.exit(1)

    # Remove existing esp32 dir (except custom files already backed up)
    if os.path.exists(ESP32_DIR):
        shutil.rmtree(ESP32_DIR)

    shutil.move(extracted_dir, ESP32_DIR)
    print(f"  Moved to: {ESP32_DIR}")

    # Cleanup temp
    if os.path.exists(temp_extract):
        shutil.rmtree(temp_extract)

    # Step 5: Restore custom files
    print("\nRestoring custom files...")
    for custom in CUSTOM_FILES:
        src = os.path.join(backup_dir, custom)
        dst = os.path.join(SCRIPT_DIR, custom)
        if os.path.exists(src):
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"  Restored: {custom}")

    # Cleanup backup
    shutil.rmtree(backup_dir)

    # Step 6: Patch platform.txt
    print("\nPatching platform.txt...")
    platform_txt = os.path.join(ESP32_DIR, "platform.txt")
    if os.path.exists(platform_txt):
        with open(platform_txt, 'r') as f:
            content = f.read()
        content = content.replace(
            "name=ESP32 Arduino",
            "name=bpad proto1 (ESP32 v2.0.17)"
        )
        content = content.replace(
            f"version={ESP32_VERSION}",
            "version=0.1.0"
        )
        with open(platform_txt, 'w') as f:
            f.write(content)
        print("  Patched name and version in platform.txt")
    else:
        print("  WARNING: platform.txt not found!")

    print()
    print("=" * 60)
    print("Setup complete!")
    print()
    print("Next steps:")
    print("  1. Test locally by copying esp32/ to:")
    print("     %LOCALAPPDATA%\\Arduino15\\packages\\bpad_proto1\\hardware\\esp32\\0.1.0\\")
    print("  2. Or run 'python build.py' to create a release zip")
    print("=" * 60)


if __name__ == "__main__":
    main()
