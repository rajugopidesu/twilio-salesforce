#!/usr/bin/env python3
"""
Setup script for Twilio Transcription Service
Runs the specific installation commands for Whisper and PyTorch
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Twilio Transcription Service")
    print("=" * 50)
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip is not available. Please install pip first.")
        return False
    
    # Install packages in the specific order you requested
    commands = [
        ("pip install git+https://github.com/openai/whisper.git", "Installing Whisper from GitHub"),
        ("pip install torch", "Installing PyTorch"),
        ("pip install -r requirements.txt", "Installing other dependencies")
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"⚠️  Continuing with next command...")
    
    print("\n" + "=" * 50)
    print(f"📊 Setup Summary: {success_count}/{len(commands)} commands completed")
    
    if success_count == len(commands):
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Test: python test_api.py")
        print("3. Deploy to Render using render.yaml")
    else:
        print("⚠️  Some installations failed. Check the errors above.")
        print("You may need to install dependencies manually.")
    
    return success_count == len(commands)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 