#!/usr/bin/env python3
"""
Test Script for File Organizer v1.0
Creates sample files and tests the organization functionality
"""

import os
import shutil
import tempfile
from pathlib import Path

def create_test_environment():
    """Create a test directory with sample files"""
    
    # Create test directory
    test_dir = "test_files"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    print(f"📁 Created test directory: {test_dir}")
    
    # Sample files to create
    sample_files = {
        # Images
        "vacation_photo.jpg": b"fake image content",
        "screenshot.png": b"fake png content",
        "animated.gif": b"fake gif content",
        "profile.webp": b"fake webp content",
        
        # Documents
        "report.pdf": b"fake pdf content",
        "letter.docx": b"fake word content",
        "notes.txt": b"These are some test notes for the organizer",
        "spreadsheet.xlsx": b"fake excel content",
        "presentation.pptx": b"fake powerpoint content",
        
        # Videos
        "movie.mp4": b"fake video content",
        "tutorial.avi": b"fake avi content",
        "stream.mkv": b"fake mkv content",
        
        # Audio
        "song.mp3": b"fake mp3 content",
        "podcast.wav": b"fake wav content",
        "music.flac": b"fake flac content",
        
        # Archives
        "backup.zip": b"fake zip content",
        "archive.rar": b"fake rar content",
        "compressed.7z": b"fake 7z content",
        
        # Code
        "script.py": b"# This is a Python script\nprint('Hello World')",
        "webpage.html": b"<html><body><h1>Test Page</h1></body></html>",
        "styles.css": b"body { font-family: Arial; }",
        "app.js": b"console.log('Hello JavaScript');",
        
        # Others (unknown extensions)
        "unknown.xyz": b"unknown file type",
        "mystery.abc": b"mystery file content",
        "random.123": b"random content",
        
        # Files without extensions
        "no_extension": b"file without extension",
        "README": b"This is a readme file"
    }
    
    # Create all sample files
    for filename, content in sample_files.items():
        file_path = os.path.join(test_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"📄 Created: {filename}")
    
    print(f"\n✅ Created {len(sample_files)} test files in '{test_dir}' directory")
    print("\nTest files created:")
    print("-" * 40)
    
    # Group files by expected category
    categories = {
        "Images": ["vacation_photo.jpg", "screenshot.png", "animated.gif", "profile.webp"],
        "Documents": ["report.pdf", "letter.docx", "notes.txt", "spreadsheet.xlsx", "presentation.pptx"],
        "Videos": ["movie.mp4", "tutorial.avi", "stream.mkv"],
        "Audio": ["song.mp3", "podcast.wav", "music.flac"],
        "Archives": ["backup.zip", "archive.rar", "compressed.7z"],
        "Code": ["script.py", "webpage.html", "styles.css", "app.js"],
        "Others": ["unknown.xyz", "mystery.abc", "random.123", "no_extension", "README"]
    }
    
    for category, files in categories.items():
        print(f"📁 {category}: {', '.join(files)}")
    
    return test_dir

def create_test_config():
    """Create a test configuration file"""
    test_config = {
        "target_directory": "./test_files",
        "rules": {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb"],
            "Others": []
        }
    }
    
    import json
    with open("test_config.json", "w") as f:
        json.dump(test_config, f, indent=4)
    
    print("⚙️ Created test_config.json")
    return "test_config.json"

def run_tests():
    """Run the complete test suite"""
    print("🧪 FILE ORGANIZER TEST SUITE")
    print("=" * 50)
    
    # Step 1: Create test environment
    print("\n1️⃣ Creating test environment...")
    test_dir = create_test_environment()
    
    # Step 2: Create test configuration
    print(f"\n2️⃣ Creating test configuration...")
    config_file = create_test_config()
    
    # Step 3: Run preview mode
    print(f"\n3️⃣ Running preview mode...")
    print("-" * 30)
    print("Command: python organizer.py --config test_config.json --preview")
    print("Expected: Should show what files would be moved without actually moving them")
    
    # Step 4: Instructions for manual testing
    print(f"\n4️⃣ Manual testing instructions:")
    print("-" * 30)
    print("Now run these commands to test the organizer:")
    print()
    print("📋 PREVIEW TEST (Safe):")
    print("   python organizer.py --config test_config.json --preview")
    print()
    print("🗂️ ACTUAL ORGANIZATION:")
    print("   python organizer.py --config test_config.json")
    print()
    print("📊 VIEW LOGS:")
    print("   python log_viewer.py")
    print()
    print("⚙️ TEST CONFIGURATION TOOL:")
    print("   python config_setup.py")
    print()
    
    # Step 5: Validation checklist
    print("5️⃣ Validation Checklist:")
    print("-" * 30)
    validation_steps = [
        "✅ Preview shows correct file categorization",
        "✅ All files are moved to correct folders",
        "✅ Folders are created automatically",
        "✅ Files with conflicts are renamed properly",
        "✅ Unknown file types go to 'Others' folder",
        "✅ Log file is created with correct entries",
        "✅ Log viewer displays information correctly",
        "✅ Configuration tool works interactively"
    ]
    
    for step in validation_steps:
        print(f"   {step}")
    
    # Step 6: Cleanup instructions
    print(f"\n6️⃣ Cleanup (when testing complete):")
    print("-" * 30)
    print("   Remove test files:")
    print(f"   - Delete '{test_dir}' directory")
    print(f"   - Delete '{config_file}'")
    print("   - Delete 'log.txt' (if you want)")
    
    print(f"\n🎉 Test environment ready!")
    print(f"📁 Test directory: {os.path.abspath(test_dir)}")
    print(f"⚙️ Test config: {os.path.abspath(config_file)}")

def cleanup_tests():
    """Clean up test files and directories"""
    items_to_remove = ["test_files", "test_config.json"]
    
    print("🧹 CLEANING UP TEST FILES")
    print("-" * 30)
    
    for item in items_to_remove:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"🗑️ Removed directory: {item}")
            else:
                os.remove(item)
                print(f"🗑️ Removed file: {item}")
        else:
            print(f"⚪ Not found: {item}")
    
    # Ask about log.txt
    if os.path.exists("log.txt"):
        response = input("\n🗑️ Remove log.txt? (y/n): ").lower()
        if response == 'y':
            os.remove("log.txt")
            print("🗑️ Removed: log.txt")
        else:
            print("⚪ Kept: log.txt")
    
    print("\n✅ Cleanup complete!")

def main():
    """Main test function with menu"""
    while True:
        print("\n" + "="*50)
        print("🧪 FILE ORGANIZER TEST SUITE")
        print("="*50)
        print("1. 🏗️  Create test environment")
        print("2. 🧹 Clean up test files")
        print("3. 📋 Show test instructions")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_tests()
        elif choice == "2":
            cleanup_tests()
        elif choice == "3":
            print("\n📋 TESTING WORKFLOW:")
            print("-" * 20)
            print("1. Run: python test_organizer.py")
            print("2. Choose option 1 to create test files")
            print("3. Test preview: python organizer.py --config test_config.json --preview")
            print("4. Test organize: python organizer.py --config test_config.json")
            print("5. Check logs: python log_viewer.py")
            print("6. Test config tool: python config_setup.py")
            print("7. Clean up: python test_organizer.py (option 2)")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()