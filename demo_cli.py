#!/usr/bin/env python3
"""
Demo Script for File Organizer v2.0 Enhanced CLI
Demonstrates the main features and functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the package to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from file_organizer.core.organizer import FileOrganizer
from file_organizer.core.config_manager import ConfigManager
from file_organizer.core.logger import Logger
from file_organizer.utils.cli import CLI, Colors

def create_demo_files(demo_dir: Path):
    """Create demo files for testing"""
    CLI.print_info("Creating demo files...")
    
    # Create various file types
    files = [
        ("document.pdf", b"PDF document"),
        ("photo.jpg", b"JPEG image"), 
        ("music.mp3", b"MP3 audio"),
        ("video.mp4", b"MP4 video"),
        ("script.py", b"print('Hello World')"),
        ("data.csv", b"name,age\nJohn,25"),
        ("archive.zip", b"ZIP archive"),
        ("presentation.pptx", b"PowerPoint"),
        ("spreadsheet.xlsx", b"Excel file"),
        ("readme.txt", b"Text file"),
    ]
    
    for filename, content in files:
        (demo_dir / filename).write_bytes(content)
    
    CLI.print_success(f"Created {len(files)} demo files")

def demo_basic_organization():
    """Demo basic file organization"""
    CLI.print_header("📁 DEMO: BASIC FILE ORGANIZATION")
    
    # Create demo directory
    demo_dir = Path(tempfile.mkdtemp(prefix="file_organizer_demo_"))
    CLI.print_info(f"Demo directory: {demo_dir}")
    
    # Create demo files
    create_demo_files(demo_dir)
    
    # Set up organizer
    config_manager = ConfigManager()
    logger = Logger()
    organizer = FileOrganizer(config_manager, logger)
    
    try:
        # Create default profile
        CLI.print_info("Creating default profile...")
        default_profile = config_manager.create_default_profile()
        if default_profile:
            CLI.print_success("Default profile created")
        
        # Preview organization
        CLI.print_section("🔍 Preview Mode")
        stats = organizer.organize_directory(
            target_directory=str(demo_dir),
            dry_run=True
        )
        
        if stats:
            CLI.print_success(f"Preview complete - Would organize {stats.total_files} files")
        
        # Organize files
        CLI.print_section("⚡ Organizing Files")
        stats = organizer.organize_directory(
            target_directory=str(demo_dir),
            dry_run=False,
            enable_undo=True
        )
        
        if stats:
            CLI.print_success(f"Organization complete! Moved {stats.files_moved} files")
            
            # Show results
            CLI.print_section("📊 Results")
            CLI.print_info("Organized folder structure:")
            for item in sorted(demo_dir.iterdir()):
                if item.is_dir():
                    file_count = len(list(item.iterdir()))
                    CLI.print_info(f"  📁 {item.name}/ ({file_count} files)")
    
    except Exception as e:
        CLI.print_error(f"Demo failed: {e}")
    
    finally:
        # Cleanup
        CLI.print_info("Cleaning up demo files...")
        shutil.rmtree(demo_dir)
        CLI.print_success("Demo cleanup complete")

def demo_profile_management():
    """Demo profile management features"""
    CLI.print_header("👤 DEMO: PROFILE MANAGEMENT")
    
    config_manager = ConfigManager()
    
    # Create different profiles
    CLI.print_info("Creating specialized profiles...")
    
    profiles = ["photographer", "developer", "student", "business"]
    for profile_type in profiles:
        profile = config_manager.create_profile_for_use_case(profile_type)
        if profile:
            CLI.print_success(f"✅ Created {profile_type} profile")
        else:
            CLI.print_error(f"❌ Failed to create {profile_type} profile")
    
    # List profiles
    CLI.print_section("📋 Available Profiles")
    profile_list = config_manager.get_profile_list()
    for profile_name in profile_list:
        profile = config_manager.get_profile(profile_name)
        if profile:
            CLI.print_info(f"• {profile.name}: {profile.description}")
            CLI.print_info(f"  Rules: {len(profile.rules)}")
            CLI.print_info(f"  Method: {profile.organize_by.value}")

def demo_cli_features():
    """Demo CLI visual features"""
    CLI.print_header("🎨 DEMO: CLI FEATURES")
    
    # Test different message types
    CLI.print_section("💬 Message Types")
    CLI.print_success("✅ Success message")
    CLI.print_info("ℹ️ Info message") 
    CLI.print_warning("⚠️ Warning message")
    CLI.print_error("❌ Error message")
    
    # Test progress bar
    CLI.print_section("📊 Progress Bar")
    import time
    progress = CLI.create_progress_bar(100, "Processing")
    for i in range(0, 101, 5):
        progress.update(i)
        time.sleep(0.1)
    progress.finish()
    CLI.print_success("Progress complete!")
    
    # Test statistics display
    CLI.print_section("📈 Statistics Display")
    sample_stats = {
        "Documents": 45,
        "Images": 32,
        "Videos": 12,
        "Audio": 8,
        "Code": 23,
        "Archives": 5
    }
    CLI.print_statistics(sample_stats)

def main():
    """Run all demos"""
    CLI.clear_screen()
    CLI.print_logo()
    
    print(f"{Colors.BRIGHT_CYAN}")
    print("=" * 80)
    print("FILE ORGANIZER v2.0 - ENHANCED CLI DEMONSTRATION")
    print("=" * 80)
    print(f"{Colors.RESET}")
    
    demos = [
        ("Basic File Organization", demo_basic_organization),
        ("Profile Management", demo_profile_management), 
        ("CLI Features", demo_cli_features),
    ]
    
    for demo_name, demo_func in demos:
        try:
            CLI.print_info(f"▶️ Starting demo: {demo_name}")
            demo_func()
            CLI.print_success(f"✅ Completed demo: {demo_name}")
            
        except Exception as e:
            CLI.print_error(f"❌ Demo failed: {demo_name} - {e}")
        
        print()
    
    CLI.print_header("🎉 DEMONSTRATION COMPLETE")
    CLI.print_success("File Organizer v2.0 Enhanced CLI is ready to use!")
    
    CLI.print_section("🚀 Quick Start")
    CLI.print_info("Try these commands:")
    CLI.print_info("• python file_organizer_cli.py --help")
    CLI.print_info("• python file_organizer_cli.py organize --preview --path ~/Downloads")
    CLI.print_info("• python file_organizer_cli.py profiles --list")
    CLI.print_info("• python file_organizer_cli.py config --create photographer")

if __name__ == "__main__":
    main()