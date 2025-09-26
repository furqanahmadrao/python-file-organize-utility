#!/usr/bin/env python3
"""
FileNest Configuration Setup
Interactive CLI for creating and editing config.json
"""

import os
import json
from pathlib import Path
from typing import Dict, List
import argparse

class ConfigSetup:
    """Interactive configuration setup for FileNest"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_existing_config()
    
    def load_existing_config(self) -> Dict:
        """Load existing config or return defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading existing config: {e}")
        
        return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "target_path": self.get_default_downloads_path(),
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
    
    def get_default_downloads_path(self) -> str:
        """Get platform-appropriate default downloads path"""
        return str(Path.home() / "Downloads")
    
    def interactive_setup(self):
        """Run interactive configuration setup"""
        print("=== FileNest Configuration Setup ===")
        print(f"Current config file: {self.config_path}")
        print()
        
        # Target path setup
        self.setup_target_path()
        
        # Categories setup
        self.setup_categories()
        
        # Advanced options
        self.setup_advanced_options()
        
        # Save configuration
        self.save_config()
        
        print("\n=== Configuration Complete ===")
        print(f"Configuration saved to: {self.config_path}")
        print("You can now run 'organize' to start organizing files!")
    
    def setup_target_path(self):
        """Setup target directory for organization"""
        print("--- Target Directory Setup ---")
        current_path = self.config.get('target_path', self.get_default_downloads_path())
        print(f"Current target directory: {current_path}")
        
        while True:
            new_path = input(f"Enter new target directory (or press Enter to keep current): ").strip()
            
            if not new_path:
                break  # Keep current
            
            # Expand user path
            expanded_path = os.path.expanduser(new_path)
            
            if os.path.exists(expanded_path):
                self.config['target_path'] = expanded_path
                print(f"✓ Target directory set to: {expanded_path}")
                break
            else:
                create = input(f"Directory '{expanded_path}' does not exist. Create it? (y/N): ").strip().lower()
                if create in ('y', 'yes'):
                    try:
                        os.makedirs(expanded_path, exist_ok=True)
                        self.config['target_path'] = expanded_path
                        print(f"✓ Created and set target directory: {expanded_path}")
                        break
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                else:
                    print("Please enter a valid directory path.")
    
    def setup_categories(self):
        """Setup file categories and extensions"""
        print("\n--- File Categories Setup ---")
        print("Current categories:")
        
        for i, (category, extensions) in enumerate(self.config['categories'].items(), 1):
            ext_display = ', '.join(extensions[:5])
            if len(extensions) > 5:
                ext_display += f" ... (+{len(extensions)-5} more)"
            print(f"  {i}. {category}: {ext_display}")
        
        print("\nOptions:")
        print("  1. Keep current categories")
        print("  2. Add new category")
        print("  3. Modify existing category")
        print("  4. Remove category")
        print("  5. Reset to defaults")
        
        while True:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                break  # Keep current
            elif choice == '2':
                self.add_category()
            elif choice == '3':
                self.modify_category()
            elif choice == '4':
                self.remove_category()
            elif choice == '5':
                self.config['categories'] = self.get_default_config()['categories']
                print("✓ Reset categories to defaults")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
    
    def add_category(self):
        """Add a new file category"""
        print("\n--- Add New Category ---")
        
        category_name = input("Enter category name: ").strip()
        if not category_name:
            print("Category name cannot be empty.")
            return
        
        if category_name in self.config['categories']:
            print(f"Category '{category_name}' already exists.")
            return
        
        print("Enter file extensions (including the dot, e.g., .txt)")
        print("Enter one extension per line. Press Enter on empty line to finish.")
        
        extensions = []
        while True:
            ext = input("Extension: ").strip()
            if not ext:
                break
            
            if not ext.startswith('.'):
                ext = '.' + ext
            
            extensions.append(ext.lower())
        
        if extensions:
            self.config['categories'][category_name] = extensions
            print(f"✓ Added category '{category_name}' with {len(extensions)} extensions")
        else:
            print("No extensions added. Category not created.")
    
    def modify_category(self):
        """Modify an existing category"""
        print("\n--- Modify Category ---")
        
        categories = list(self.config['categories'].keys())
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category}")
        
        try:
            choice = int(input("Select category to modify (number): ")) - 1
            if 0 <= choice < len(categories):
                category_name = categories[choice]
                
                current_extensions = self.config['categories'][category_name]
                print(f"Current extensions for '{category_name}': {', '.join(current_extensions)}")
                
                print("Enter new extensions (including the dot, e.g., .txt)")
                print("Press Enter on empty line to finish.")
                
                extensions = []
                while True:
                    ext = input("Extension: ").strip()
                    if not ext:
                        break
                    
                    if not ext.startswith('.'):
                        ext = '.' + ext
                    
                    extensions.append(ext.lower())
                
                if extensions:
                    self.config['categories'][category_name] = extensions
                    print(f"✓ Updated category '{category_name}' with {len(extensions)} extensions")
                else:
                    print("No extensions provided. Category unchanged.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    def remove_category(self):
        """Remove a category"""
        print("\n--- Remove Category ---")
        
        categories = list(self.config['categories'].keys())
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category}")
        
        try:
            choice = int(input("Select category to remove (number): ")) - 1
            if 0 <= choice < len(categories):
                category_name = categories[choice]
                
                confirm = input(f"Remove category '{category_name}'? (y/N): ").strip().lower()
                if confirm in ('y', 'yes'):
                    del self.config['categories'][category_name]
                    print(f"✓ Removed category '{category_name}'")
                else:
                    print("Category not removed.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    def setup_advanced_options(self):
        """Setup advanced configuration options"""
        print("\n--- Advanced Options ---")
        
        # Others folder name
        current_others = self.config.get('others_folder', 'Others')
        others_folder = input(f"Folder name for uncategorized files [{current_others}]: ").strip()
        if others_folder:
            self.config['others_folder'] = others_folder
        
        # Duplicate strategy
        current_strategy = self.config.get('duplicate_strategy', 'rename')
        print(f"\nDuplicate file handling (current: {current_strategy}):")
        print("  1. rename - Add (1), (2), etc. to filename")
        print("  2. skip - Skip files that already exist")  
        print("  3. overwrite - Replace existing files")
        
        strategy_choice = input("Choose strategy (1-3) or press Enter to keep current: ").strip()
        strategy_map = {'1': 'rename', '2': 'skip', '3': 'overwrite'}
        if strategy_choice in strategy_map:
            self.config['duplicate_strategy'] = strategy_map[strategy_choice]
        
        # Move empty folders
        current_move_empty = self.config.get('move_empty_folders', False)
        move_empty = input(f"Move empty folders? (y/N) [current: {'yes' if current_move_empty else 'no'}]: ").strip().lower()
        if move_empty in ('y', 'yes'):
            self.config['move_empty_folders'] = True
        elif move_empty in ('n', 'no'):
            self.config['move_empty_folders'] = False
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Configuration saved to: {self.config_path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def import_config(self, import_path: str):
        """Import configuration from file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config has required fields
            required_fields = ['target_path', 'categories']
            for field in required_fields:
                if field not in imported_config:
                    print(f"Error: Imported config missing required field: {field}")
                    return False
            
            self.config = imported_config
            self.save_config()
            print(f"✓ Configuration imported from: {import_path}")
            return True
            
        except Exception as e:
            print(f"Error importing configuration: {e}")
            return False
    
    def show_current_config(self):
        """Display current configuration"""
        print("=== Current Configuration ===")
        print(f"Target Path: {self.config.get('target_path', 'Not set')}")
        print(f"Others Folder: {self.config.get('others_folder', 'Others')}")
        print(f"Duplicate Strategy: {self.config.get('duplicate_strategy', 'rename')}")
        print(f"Move Empty Folders: {self.config.get('move_empty_folders', False)}")
        
        print("\nCategories:")
        for category, extensions in self.config.get('categories', {}).items():
            ext_display = ', '.join(extensions[:5])
            if len(extensions) > 5:
                ext_display += f" ... (+{len(extensions)-5} more)"
            print(f"  {category}: {ext_display}")

def main():
    """Main CLI entry point for config setup"""
    parser = argparse.ArgumentParser(
        prog='config_setup',
        description='FileNest Configuration Setup',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--import', dest='import_file', type=str, 
                       help='Import configuration from JSON file')
    parser.add_argument('--config', type=str, default='config.json',
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--show', action='store_true',
                       help='Show current configuration')
    
    args = parser.parse_args()
    
    # Create config setup instance
    setup = ConfigSetup(args.config)
    
    if args.show:
        setup.show_current_config()
    elif args.import_file:
        setup.import_config(args.import_file)
    else:
        setup.interactive_setup()

if __name__ == "__main__":
    main()