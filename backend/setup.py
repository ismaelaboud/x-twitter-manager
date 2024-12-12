import subprocess
import sys
import os

def install_dependencies():
    """Install only essential dependencies"""
    dependencies = [
        'openai==1.3.7',  # Latest version with new API
        'python-dotenv',
        'httpx==0.24.1',  # Specific version to avoid proxy issues
        'requests',  # Lightweight alternative for HTTP requests
        'textblob',   # For sentiment analysis
        
        # Hugging Face Dependencies
        'transformers==4.35.2',
        'torch==2.3.1',  # Updated to latest stable version
        'huggingface_hub==0.19.4'
        # Removed sentencepiece to avoid build issues
    ]
    
    for package in dependencies:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def upgrade_pip():
    """Upgrade pip to latest version"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print("🆙 Pip upgraded successfully")
    except Exception as e:
        print(f"❌ Pip upgrade failed: {e}")

def install_build_tools_hint():
    """Provide guidance for installing build tools"""
    print("\n🛠️ IMPORTANT: If you encounter build errors, install Microsoft C++ Build Tools:")
    print("1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    print("2. During installation, select 'Desktop development with C++'")
    print("3. Ensure 'MSVC v143 - VS 2022 C++ x64/x86 build tools' is checked\n")

if __name__ == "__main__":
    print("🚀 Setting up dependencies for X-Twitter Bot...")
    
    # Upgrade pip first
    upgrade_pip()
    
    # Install dependencies
    try:
        install_dependencies()
        print("🎉 Setup complete!")
    except Exception as e:
        print(f"❌ Setup encountered an error: {e}")
        install_build_tools_hint()
