#!/usr/bin/env python3
"""
FileNest Build Script
Automated build script for creating distributions
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

class FileNestBuilder:
    """Build automation for FileNest"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        
    def clean_build(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  Removed: {dir_path}")
        
        # Remove egg-info directories
        for egg_info in self.project_dir.glob("*.egg-info"):
            shutil.rmtree(egg_info)
            print(f"  Removed: {egg_info}")
    
    def install_build_dependencies(self):
        """Install required build dependencies"""
        print("📦 Installing build dependencies...")
        
        dependencies = [
            "build",
            "wheel", 
            "twine",
            "pyinstaller",
            "watchdog",  # Optional dependency
        ]
        
        for dep in dependencies:
            print(f"  Installing {dep}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True, text=True)
                print(f"  ✓ {dep} installed")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to install {dep}: {e}")
    
    def build_wheel(self):
        """Build wheel distribution"""
        print("🎯 Building wheel distribution...")
        
        try:
            subprocess.run([sys.executable, "-m", "build"], 
                         cwd=self.project_dir, check=True)
            print("  ✓ Wheel built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Wheel build failed: {e}")
            return False
    
    def build_executable(self):
        """Build standalone executable with PyInstaller"""
        print("🔨 Building standalone executable...")
        
        spec_file = self.project_dir / "filenest.spec"
        
        if not spec_file.exists():
            print("  ❌ filenest.spec not found")
            return False
        
        try:
            subprocess.run([
                "pyinstaller", 
                "--clean",
                str(spec_file)
            ], cwd=self.project_dir, check=True)
            
            print("  ✓ Executable built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Executable build failed: {e}")
            return False
    
    def test_builds(self):
        """Test the built distributions"""
        print("🧪 Testing builds...")
        
        # Test wheel installation in virtual environment
        test_env = self.project_dir / "test_env"
        
        try:
            # Create test environment
            subprocess.run([sys.executable, "-m", "venv", str(test_env)], check=True)
            
            # Determine pip path based on platform
            if platform.system() == "Windows":
                pip_path = test_env / "Scripts" / "pip.exe"
            else:
                pip_path = test_env / "bin" / "pip"
            
            # Find the built wheel
            wheel_files = list(self.dist_dir.glob("*.whl"))
            if wheel_files:
                wheel_path = wheel_files[0]
                
                # Install the wheel
                subprocess.run([str(pip_path), "install", str(wheel_path)], check=True)
                print("  ✓ Wheel installation test passed")
            
            # Clean up test environment
            shutil.rmtree(test_env)
            
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Test failed: {e}")
        except Exception as e:
            print(f"  ⚠️ Test error: {e}")
    
    def create_release_package(self):
        """Create a complete release package"""
        print("📋 Creating release package...")
        
        release_dir = self.project_dir / "release"
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir()
        
        # Copy important files
        files_to_copy = [
            "readme_docs.md",
            "LICENSE",  # If exists
            "requirements.txt",  # If exists
        ]
        
        for file_name in files_to_copy:
            src_path = self.project_dir / file_name
            if src_path.exists():
                shutil.copy2(src_path, release_dir)
        
        # Copy built distributions
        if self.dist_dir.exists():
            for dist_file in self.dist_dir.iterdir():
                if dist_file.is_file():
                    shutil.copy2(dist_file, release_dir)
        
        # Create install instructions
        install_instructions = release_dir / "INSTALL.md"
        with open(install_instructions, 'w') as f:
            f.write(self.get_install_instructions())
        
        print(f"  ✓ Release package created in: {release_dir}")
    
    def get_install_instructions(self) -> str:
        """Generate installation instructions"""
        return """# FileNest Installation Instructions

## Method 1: Install from Wheel (Recommended)

```bash
pip install filenest-1.0.0-py3-none-any.whl
```

After installation, you can use:
- `organize` - Main file organization command
- `config-setup` - Interactive configuration
- `log-viewer` - View operation logs

## Method 2: Standalone Executable

Use the `filenest.exe` (Windows) or `filenest` (Linux/macOS) executable directly.
No Python installation required!

```bash
# Windows
filenest.exe --help

# Linux/macOS
./filenest --help
```

## Method 3: Install with Watch Support

For real-time file monitoring:

```bash
pip install filenest-1.0.0-py3-none-any.whl[watch]
```

## Quick Start

1. Set up configuration:
   ```bash
   config-setup
   ```

2. Organize your Downloads folder:
   ```bash
   organize
   ```

3. Watch for new files automatically:
   ```bash
   organize --watch
   ```

4. View operation logs:
   ```bash
   log-viewer
   ```

For more information, see readme_docs.md
"""
    
    def build_all(self):
        """Build all distribution formats"""
        print("🚀 Starting FileNest build process...")
        print(f"Project directory: {self.project_dir}")
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print("=" * 60)
        
        success_count = 0
        total_steps = 0
        
        # Clean previous builds
        self.clean_build()
        
        # Install dependencies
        self.install_build_dependencies()
        
        # Build wheel
        total_steps += 1
        if self.build_wheel():
            success_count += 1
        
        # Build executable
        total_steps += 1 
        if self.build_executable():
            success_count += 1
        
        # Test builds
        self.test_builds()
        
        # Create release package
        self.create_release_package()
        
        # Summary
        print("=" * 60)
        print(f"🎉 Build completed: {success_count}/{total_steps} successful")
        
        if self.dist_dir.exists():
            print(f"\nBuilt files:")
            for file_path in self.dist_dir.iterdir():
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"  📁 {file_path.name} ({size_mb:.1f} MB)")
        
        print(f"\n📦 Release package: {self.project_dir / 'release'}")
        print("\n✨ Ready for distribution!")

def main():
    """Main build script entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        builder = FileNestBuilder()
        
        if command == "clean":
            builder.clean_build()
        elif command == "wheel":
            builder.build_wheel()
        elif command == "exe":
            builder.build_executable()
        elif command == "test":
            builder.test_builds()
        elif command == "release":
            builder.create_release_package()
        elif command == "all":
            builder.build_all()
        else:
            print("Unknown command. Available: clean, wheel, exe, test, release, all")
    else:
        # Default: build all
        builder = FileNestBuilder()
        builder.build_all()

if __name__ == "__main__":
    main()