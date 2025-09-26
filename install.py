#!/usr/bin/env python3
"""
FileNest Quick Installer
One-click installation script for FileNest
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class FileNestInstaller:
    """Quick installer for FileNest"""
    
    def __init__(self):
        self.python_exe = sys.executable
        self.platform = platform.system()
        self.install_dir = Path.home() / ".filenest"
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Error: Python 3.8 or higher is required")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            print("   Please upgrade Python and try again.")
            return False
        
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    
    def install_filenest(self):
        """Install FileNest using pip"""
        print("📦 Installing FileNest...")
        
        try:
            # Try to install from current directory if setup.py exists
            if (Path.cwd() / "setup.py").exists():
                print("  Installing from local source...")
                result = subprocess.run([
                    self.python_exe, "-m", "pip", "install", "-e", ".[all]"
                ], capture_output=True, text=True)
            else:
                # Install from PyPI (when available)
                print("  Installing from PyPI...")
                result = subprocess.run([
                    self.python_exe, "-m", "pip", "install", "filenest[all]"
                ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✓ FileNest installed successfully!")
                return True
            else:
                print(f"  ❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Installation error: {e}")
            return False
    
    def setup_initial_config(self):
        """Set up initial configuration"""
        print("⚙️ Setting up initial configuration...")
        
        # Create install directory
        self.install_dir.mkdir(exist_ok=True)
        
        # Default configuration
        default_config = {
            "target_path": str(Path.home() / "Downloads"),
            "categories": {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
                "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
                "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v"],
                "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
                "Software": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".appimage"],
                "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".go", ".rs"]
            },
            "others_folder": "Others",
            "move_empty_folders": False,
            "duplicate_strategy": "rename"
        }
        
        config_path = self.install_dir / "config.json"
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"  ✓ Configuration saved to: {config_path}")
            return True
            
        except Exception as e:
            print(f"  ❌ Config setup failed: {e}")
            return False
    
    def test_installation(self):
        """Test the installation"""
        print("🧪 Testing installation...")
        
        commands_to_test = ["organize", "config-setup", "log-viewer"]
        
        for command in commands_to_test:
            try:
                result = subprocess.run([
                    command, "--help"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"  ✓ {command} - Working")
                else:
                    print(f"  ⚠️ {command} - Issue detected")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⚠️ {command} - Timeout")
            except FileNotFoundError:
                print(f"  ❌ {command} - Not found")
            except Exception as e:
                print(f"  ❌ {command} - Error: {e}")
    
    def create_desktop_shortcuts(self):
        """Create desktop shortcuts (Windows only for now)"""
        if self.platform != "Windows":
            return
        
        print("🖥️ Creating desktop shortcuts...")
        
        try:
            import win32com.client
            
            desktop = Path.home() / "Desktop"
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Create shortcut for organize command
            shortcut_path = desktop / "FileNest Organize.lnk"
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = self.python_exe
            shortcut.Arguments = "-m organizer"
            shortcut.WorkingDirectory = str(Path.home())
            shortcut.IconLocation = self.python_exe
            shortcut.save()
            
            print(f"  ✓ Desktop shortcut created: {shortcut_path.name}")
            
        except ImportError:
            print("  ⚠️ pywin32 not available - skipping shortcuts")
        except Exception as e:
            print(f"  ⚠️ Shortcut creation failed: {e}")
    
    def show_success_message(self):
        """Show installation success message"""
        print("\n" + "=" * 60)
        print("🎉 FileNest Installation Complete!")
        print("=" * 60)
        
        print("\n📋 Quick Start:")
        print("  1. Configure FileNest:")
        print("     config-setup")
        print()
        print("  2. Organize your Downloads folder:")
        print("     organize")
        print()
        print("  3. Watch for new files automatically:")
        print("     organize --watch")
        print()
        print("  4. View operation logs:")
        print("     log-viewer")
        print()
        
        print("📁 Configuration stored in:")
        print(f"   {self.install_dir}")
        print()
        
        print("💡 Tips:")
        print("   • Use 'organize --dry-run' to preview changes")
        print("   • Use 'organize --path /custom/path' for other directories")
        print("   • Use 'config-setup' to modify categories anytime")
        print()
        
        print("✨ Happy organizing!")
    
    def install(self):
        """Run the complete installation process"""
        print("🚀 FileNest Quick Installer")
        print("=" * 60)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install FileNest
        if not self.install_filenest():
            return False
        
        # Setup initial configuration
        if not self.setup_initial_config():
            print("⚠️ Warning: Configuration setup failed, but installation succeeded")
        
        # Test installation
        self.test_installation()
        
        # Create shortcuts (Windows only)
        self.create_desktop_shortcuts()
        
        # Show success message
        self.show_success_message()
        
        return True

def main():
    """Main installer entry point"""
    installer = FileNestInstaller()
    
    try:
        success = installer.install()
        if not success:
            print("\n❌ Installation failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()