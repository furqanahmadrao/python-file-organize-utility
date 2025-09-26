#!/usr/bin/env python3
"""
Virtual Environment Activation Script for File Organizer v1.0
Run this script to activate the virtual environment and show usage instructions
"""

import os
import sys
import subprocess
import platform

def main():
    print("🗂️  FILE ORGANIZER v1.0 - VIRTUAL ENVIRONMENT")
    print("=" * 50)
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is already activated!")
        print(f"🐍 Python path: {sys.executable}")
    else:
        print("❌ Virtual environment is not activated")
        print("\n🔧 To activate the virtual environment:")
        
        if platform.system() == "Windows":
            print("   PowerShell: .\\venv\\Scripts\\Activate.ps1")
            print("   Command Prompt: .\\venv\\Scripts\\activate.bat")
        else:
            print("   macOS/Linux: source venv/bin/activate")
        
        print("\n💡 Then run this script again to see usage instructions")
        return
    
    print(f"📁 Project Directory: {os.getcwd()}")
    print()
    
    # Show available commands
    print("📋 AVAILABLE COMMANDS:")
    print("-" * 30)
    print("🗂️  python organizer_main.py --preview    # Preview organization")
    print("🗂️  python organizer_main.py             # Organize files")
    print("⚙️  python config_setup.py               # Configure settings")
    print("📊 python log_viewer.py                 # View logs")
    print("🧪 python test_script.py                # Run tests")
    print()
    
    print("📚 QUICK START:")
    print("-" * 15)
    print("1. python test_script.py                 # Create test files")
    print("2. python organizer_main.py --preview    # Preview organization")
    print("3. python organizer_main.py             # Actually organize")
    print("4. python log_viewer.py                 # Check results")
    print()
    
    print("🛠️  ENVIRONMENT INFO:")
    print("-" * 20)
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Executable: {sys.executable}")
    
    # Check if project files exist
    required_files = ['organizer_main.py', 'config_setup.py', 'log_viewer.py', 'test_script.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"\n⚠️  WARNING: Missing files: {', '.join(missing_files)}")
    else:
        print("\n✅ All project files are present")
    
    print("\n🚀 Ready to organize files!")

if __name__ == "__main__":
    main()