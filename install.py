import subprocess
import sys
import os
import venv
from pathlib import Path

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create("venv", with_pip=True)
        return True
    return False

def get_python_executable():
    """Get the Python executable path based on the OS."""
    if sys.platform == "win32":
        return str(Path("venv") / "Scripts" / "python.exe")
    return str(Path("venv") / "bin" / "python")

def install_requirements():
    """Install all required packages."""
    python_exe = get_python_executable()
    
    print("Installing required packages...")
    try:
        # Install packages from requirements.txt
        subprocess.check_call([python_exe, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Successfully installed all required packages!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def download_nltk_data():
    """Download required NLTK data."""
    print("Downloading required NLTK data...")
    python_exe = get_python_executable()
    nltk_script = """
import nltk
required_nltk_data = ['punkt', 'punkt_tab']
for data in required_nltk_data:
    try:
        nltk.data.find(f"tokenizers/{data}")
    except LookupError:
        nltk.download(data)
"""
    try:
        subprocess.check_call([python_exe, "-c", nltk_script])
        print("Successfully downloaded NLTK data!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading NLTK data: {e}")
        sys.exit(1)

def main():
    print("=== AI Document Search Installation ===")
    
    # Create virtual environment if needed
    if create_venv():
        print("Virtual environment created successfully!")
    else:
        print("Using existing virtual environment.")
    
    # Install requirements
    install_requirements()
    
    # Download NLTK data
    download_nltk_data()
    
    print("\nInstallation completed successfully!")
    print("\nTo use the application:")
    if sys.platform == "win32":
        print("1. Activate the virtual environment: .\\venv\\Scripts\\activate")
    else:
        print("1. Activate the virtual environment: source venv/bin/activate")
    print("2. Run the application: python app.py")

if __name__ == "__main__":
    main() 