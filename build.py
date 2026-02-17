#!/usr/bin/env python3
"""
Build script for bpad_proto1_core.
Creates a release zip for distribution via Arduino Board Manager.

Usage:
    python build.py

Prerequisites:
    Run setup.py first to download and set up the ESP32 core.
"""

import os
import sys
import subprocess
import hashlib
import zipfile


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ESP32_DIR = os.path.join(SCRIPT_DIR, "esp32")
RELEASE_DIR = os.path.join(SCRIPT_DIR, "release")


def get_git_short_sha():
    """Get the short git SHA of the current commit."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True, cwd=SCRIPT_DIR
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def compute_sha256(filepath):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_zip(source_dir, zip_path):
    """Create a zip file from a directory."""
    print(f"Creating zip: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, os.path.dirname(source_dir))
                zf.write(file_path, arc_name)
    print(f"  Created: {zip_path}")


def main():
    print("=" * 60)
    print("bpad proto1 core - Build Script")
    print("=" * 60)
    print()

    # Verify esp32 directory exists
    if not os.path.exists(ESP32_DIR):
        print("ERROR: esp32/ directory not found!")
        print("Run 'python setup.py' first to download the ESP32 core.")
        sys.exit(1)

    # Check for platform.txt to verify setup was done
    platform_txt = os.path.join(ESP32_DIR, "platform.txt")
    if not os.path.exists(platform_txt):
        print("ERROR: esp32/platform.txt not found!")
        print("Run 'python setup.py' first.")
        sys.exit(1)

    # Get version from user
    version = input("Enter release version number (e.g., 0.1.0): ").strip()
    if not version:
        print("ERROR: Version cannot be empty!")
        sys.exit(1)

    version_tag = f"v{version}"

    # Get git SHA
    short_sha = get_git_short_sha()
    zip_filename = f"bpad_proto1-{version_tag}-{short_sha}.zip"

    # Create release directory
    os.makedirs(RELEASE_DIR, exist_ok=True)
    zip_path = os.path.join(RELEASE_DIR, zip_filename)

    # Show existing releases
    print(f"\nExisting releases in {RELEASE_DIR}:")
    if os.path.exists(RELEASE_DIR):
        for f in os.listdir(RELEASE_DIR):
            fpath = os.path.join(RELEASE_DIR, f)
            size_mb = os.path.getsize(fpath) / (1024 * 1024)
            print(f"  {f} ({size_mb:.1f} MB)")
    print()

    # Create zip
    create_zip(ESP32_DIR, zip_path)

    # Compute checksum
    file_sha = compute_sha256(zip_path)
    file_size = os.path.getsize(zip_path)
    file_size_mb = file_size / (1024 * 1024)

    print()
    print("=" * 60)
    print("Build complete!")
    print("=" * 60)
    print()
    print(f"  File:     {zip_filename}")
    print(f"  Size:     {file_size} bytes ({file_size_mb:.1f} MB)")
    print(f"  Checksum: SHA-256:{file_sha}")
    print()
    print("Next steps:")
    print(f"  1. Tag this commit:  git tag {version_tag}")
    print(f"  2. Push tags:        git push --tags")
    print(f"  3. Create a GitHub Release for {version_tag}")
    print(f"  4. Upload {zip_filename} to the release")
    print(f"  5. Update package_bpad_proto1_index.json with:")
    print(f'     - "version": "{version}"')
    print(f'     - "url": "<your-github-release-url>/{zip_filename}"')
    print(f'     - "archiveFileName": "{zip_filename}"')
    print(f'     - "checksum": "SHA-256:{file_sha}"')
    print(f'     - "size": "{file_size}"')
    print()


if __name__ == "__main__":
    main()
