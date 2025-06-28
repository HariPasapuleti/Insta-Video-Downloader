#!/usr/bin/env python3
"""
Script to install required dependencies for the Instagram Video Downloader project.
This script installs dependencies for both local development and production deployment.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    print("Installing dependencies for Instagram Video Downloader...")
    print("=" * 50)
    
    # Core dependencies
    dependencies = [
        "Django>=4.2.0",
        "instaloader>=4.10.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "django-dotenv>=1.4.2",
        "python-dotenv>=1.0.0",
        "djangorestframework>=3.14.0",
        "django-cors-headers>=4.3.0",
        "gunicorn>=21.2.0",
        "whitenoise>=6.6.0"
    ]
    
    success_count = 0
    total_count = len(dependencies)
    
    for package in dependencies:
        if install_package(package):
            success_count += 1
    
    print("=" * 50)
    print(f"Installation complete: {success_count}/{total_count} packages installed successfully")
    
    if success_count == total_count:
        print("✓ All dependencies installed successfully!")
        print("\nYou can now run the Django development server:")
        print("cd instavideo && python manage.py runserver")
    else:
        print("⚠ Some packages failed to install. Please check the errors above.")
        print("You may need to install them manually or check your Python environment.")

if __name__ == "__main__":
    main() 