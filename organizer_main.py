#!/usr/bin/env python3
"""
File Organizer v1.0
Automatically organizes files into categorized folders based on extensions.
"""

import os
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class FileOrganizer:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.log_file = "log.txt"
        self.moved_files = []
        self.errors = []

    def load_config(self) -> Dict:
        """Load configuration from config.json or create default"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default configuration
            default_config = {
                "target_directory": "./Downloads",
                "rules": {
                    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
                    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
                    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
                    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
                    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
                    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb"],
                    "Others": []  # Catch-all for unknown extensions
                }
            }
            self.save_config(default_config)
            print(f"✅ Created default config.json")
            return default_config
    
    def save_config(self, config: Dict):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    def get_file_category(self, file_extension: str) -> str:
        """Determine which category a file belongs to based on extension"""
        file_extension = file_extension.lower()
        
        for category, extensions in self.config["rules"].items():
            if category == "Others":
                continue
            if file_extension in [ext.lower() for ext in extensions]:
                return category
        
        return "Others"  # Default category for unknown extensions

    def create_folders(self, target_dir: str) -> List[str]:
        """Create category folders if they don't exist"""
        created_folders = []
        
        for category in self.config["rules"].keys():
            folder_path = os.path.join(target_dir, category)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                created_folders.append(category)
                print(f"📁 Created folder: {category}")
        
        return created_folders

    def handle_file_conflict(self, source: str, destination: str) -> str:
        """Handle file name conflicts by adding counter"""
        if not os.path.exists(destination):
            return destination
        
        base_name = os.path.splitext(os.path.basename(destination))[0]
        extension = os.path.splitext(destination)[1]
        directory = os.path.dirname(destination)
        
        counter = 1
        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_destination = os.path.join(directory, new_name)
            if not os.path.exists(new_destination):
                return new_destination
            counter += 1

    def move_file(self, source_path: str, target_dir: str, dry_run: bool = False) -> Tuple[bool, str]:
        """Move a single file to appropriate category folder"""
        try:
            file_name = os.path.basename(source_path)
            file_extension = os.path.splitext(file_name)[1]
            category = self.get_file_category(file_extension)
            
            destination_folder = os.path.join(target_dir, category)
            destination_path = os.path.join(destination_folder, file_name)
            
            # Handle file conflicts
            final_destination = self.handle_file_conflict(source_path, destination_path)
            final_file_name = os.path.basename(final_destination)
            
            if dry_run:
                return True, f"PREVIEW: {file_name} → {category}/{final_file_name}"
            
            # Actually move the file
            shutil.move(source_path, final_destination)
            
            # Log the move
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} | MOVED: {file_name} → {category}/{final_file_name}"
            
            return True, log_entry
            
        except Exception as e:
            error_msg = f"ERROR moving {os.path.basename(source_path)}: {str(e)}"
            return False, error_msg

    def organize_files(self, target_directory: str = None, dry_run: bool = False):
        """Main function to organize all files in target directory"""
        
        # Use config directory or provided directory
        if target_directory is None:
            target_directory = self.config["target_directory"]
        
        # Validate target directory
        if not os.path.exists(target_directory):
            print(f"❌ Target directory does not exist: {target_directory}")
            return
        
        print(f"🎯 Target Directory: {target_directory}")
        print(f"🔍 Mode: {'DRY RUN (Preview)' if dry_run else 'ORGANIZING FILES'}")
        print("-" * 50)
        
        # Create folders (unless dry run)
        if not dry_run:
            created_folders = self.create_folders(target_directory)
            if created_folders:
                print()
        
        # Get all files in target directory (not subdirectories)
        files_to_organize = [
            f for f in os.listdir(target_directory) 
            if os.path.isfile(os.path.join(target_directory, f))
        ]
        
        if not files_to_organize:
            print("📂 No files found to organize!")
            return
        
        print(f"📋 Found {len(files_to_organize)} files to organize:")
        print()
        
        # Process each file
        successful_moves = 0
        for file_name in files_to_organize:
            file_path = os.path.join(target_directory, file_name)
            success, message = self.move_file(file_path, target_directory, dry_run)
            
            if success:
                print(f"✅ {message}")
                if not dry_run:
                    self.moved_files.append(message)
                successful_moves += 1
            else:
                print(f"❌ {message}")
                self.errors.append(message)
        
        print()
        print("-" * 50)
        
        if dry_run:
            print(f"📊 PREVIEW COMPLETE: {successful_moves} files would be organized")
            print("💡 Run without --preview to actually organize files")
        else:
            print(f"🎉 ORGANIZATION COMPLETE!")
            print(f"✅ Successfully organized: {successful_moves} files")
            if self.errors:
                print(f"❌ Errors encountered: {len(self.errors)} files")
            
            # Write to log file
            self.write_log()

    def write_log(self):
        """Write all moves and errors to log file"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"ORGANIZATION SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n")
            
            for entry in self.moved_files:
                f.write(f"{entry}\n")
            
            if self.errors:
                f.write(f"\nERRORS:\n")
                for error in self.errors:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {error}\n")
            
            f.write(f"\nSUMMARY: {len(self.moved_files)} moved, {len(self.errors)} errors\n\n")

def main():
    parser = argparse.ArgumentParser(description='File Organizer v1.0 - Organize files by extension')
    parser.add_argument('--path', type=str, help='Target directory to organize (overrides config)')
    parser.add_argument('--preview', action='store_true', help='Preview mode - show what would be organized')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    
    args = parser.parse_args()
    
    print("🗂️  FILE ORGANIZER v1.0")
    print("=" * 30)
    
    # Create organizer instance
    organizer = FileOrganizer(args.config)
    
    # Run organization
    organizer.organize_files(target_directory=args.path, dry_run=args.preview)

if __name__ == "__main__":
    main()