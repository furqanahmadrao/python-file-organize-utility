#!/usr/bin/env python3
"""
Configuration Setup Tool for File Organizer v1.0
Interactive CLI tool to create and modify config.json
"""

import json
import os
from typing import Dict, List

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_or_create_config()

    def load_or_create_config(self) -> Dict:
        """Load existing config or create default"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                print(f"✅ Loaded existing config from {self.config_path}")
                return config
        except FileNotFoundError:
            print(f"📄 Creating new config file: {self.config_path}")
            return self.create_default_config()

    def create_default_config(self) -> Dict:
        """Create default configuration"""
        return {
            "target_directory": "./Downloads",
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

    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        print(f"💾 Configuration saved to {self.config_path}")

    def display_current_config(self):
        """Display current configuration in a readable format"""
        print("\n" + "="*50)
        print("📋 CURRENT CONFIGURATION")
        print("="*50)
        
        print(f"🎯 Target Directory: {self.config['target_directory']}")
        print("\n📁 Categories and Extensions:")
        
        for category, extensions in self.config["rules"].items():
            if category == "Others":
                print(f"   {category}: (catch-all for unknown extensions)")
            else:
                ext_display = ", ".join(extensions[:5])  # Show first 5
                if len(extensions) > 5:
                    ext_display += f" ... (+{len(extensions)-5} more)"
                print(f"   {category}: {ext_display}")
        print()

    def change_target_directory(self):
        """Change the target directory"""
        print("\n🎯 CHANGE TARGET DIRECTORY")
        print("-" * 30)
        
        current_dir = self.config["target_directory"]
        print(f"Current directory: {current_dir}")
        
        new_dir = input("Enter new target directory (or press Enter to keep current): ").strip()
        
        if new_dir:
            # Validate directory
            if os.path.exists(new_dir):
                self.config["target_directory"] = new_dir
                print(f"✅ Target directory changed to: {new_dir}")
            else:
                create_dir = input(f"Directory doesn't exist. Create it? (y/n): ").lower()
                if create_dir == 'y':
                    try:
                        os.makedirs(new_dir, exist_ok=True)
                        self.config["target_directory"] = new_dir
                        print(f"✅ Created and set target directory: {new_dir}")
                    except Exception as e:
                        print(f"❌ Failed to create directory: {e}")
                else:
                    print("❌ Target directory not changed")
        else:
            print("📂 Target directory unchanged")

    def add_category(self):
        """Add a new category"""
        print("\n➕ ADD NEW CATEGORY")
        print("-" * 25)
        
        category_name = input("Enter category name (e.g., 'Scripts'): ").strip()
        
        if not category_name:
            print("❌ Category name cannot be empty")
            return
        
        if category_name in self.config["rules"]:
            print(f"❌ Category '{category_name}' already exists")
            return
        
        print(f"Enter extensions for '{category_name}' category:")
        print("Format: .ext1,.ext2,.ext3 (include the dots)")
        print("Example: .py,.sh,.bat")
        
        extensions_input = input("Extensions: ").strip()
        
        if not extensions_input:
            print("❌ Extensions cannot be empty")
            return
        
        # Parse extensions
        extensions = [ext.strip() for ext in extensions_input.split(',')]
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        
        self.config["rules"][category_name] = extensions
        
        print(f"✅ Added category '{category_name}' with extensions: {', '.join(extensions)}")

    def modify_category(self):
        """Modify an existing category"""
        print("\n✏️  MODIFY EXISTING CATEGORY")
        print("-" * 30)
        
        categories = [cat for cat in self.config["rules"].keys() if cat != "Others"]
        
        if not categories:
            print("❌ No categories available to modify")
            return
        
        print("Available categories:")
        for i, category in enumerate(categories, 1):
            extensions = self.config["rules"][category]
            ext_display = ", ".join(extensions[:3])
            if len(extensions) > 3:
                ext_display += f" ... (+{len(extensions)-3} more)"
            print(f"  {i}. {category}: {ext_display}")
        
        try:
            choice = int(input("Select category number to modify: ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                
                print(f"\nModifying category: {category}")
                print(f"Current extensions: {', '.join(self.config['rules'][category])}")
                
                print("\nOptions:")
                print("1. Replace all extensions")
                print("2. Add more extensions")
                print("3. Remove extensions")
                
                action = input("Choose action (1-3): ").strip()
                
                if action == "1":
                    new_extensions = input("Enter new extensions (.ext1,.ext2): ").strip()
                    if new_extensions:
                        extensions = [ext.strip() for ext in new_extensions.split(',')]
                        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
                        self.config["rules"][category] = extensions
                        print(f"✅ Replaced extensions for '{category}'")
                
                elif action == "2":
                    add_extensions = input("Enter extensions to add (.ext1,.ext2): ").strip()
                    if add_extensions:
                        extensions = [ext.strip() for ext in add_extensions.split(',')]
                        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
                        self.config["rules"][category].extend(extensions)
                        # Remove duplicates
                        self.config["rules"][category] = list(set(self.config["rules"][category]))
                        print(f"✅ Added extensions to '{category}'")
                
                elif action == "3":
                    remove_extensions = input("Enter extensions to remove (.ext1,.ext2): ").strip()
                    if remove_extensions:
                        extensions = [ext.strip() for ext in remove_extensions.split(',')]
                        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
                        for ext in extensions:
                            if ext in self.config["rules"][category]:
                                self.config["rules"][category].remove(ext)
                        print(f"✅ Removed extensions from '{category}'")
            
            else:
                print("❌ Invalid category number")
        
        except ValueError:
            print("❌ Invalid input")

    def delete_category(self):
        """Delete an existing category"""
        print("\n🗑️  DELETE CATEGORY")
        print("-" * 20)
        
        categories = [cat for cat in self.config["rules"].keys() if cat != "Others"]
        
        if not categories:
            print("❌ No categories available to delete")
            return
        
        print("Available categories:")
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category}")
        
        try:
            choice = int(input("Select category number to delete: ")) - 1
            if 0 <= choice < len(categories):
                category = categories[choice]
                
                confirm = input(f"Are you sure you want to delete '{category}'? (y/n): ").lower()
                if confirm == 'y':
                    del self.config["rules"][category]
                    print(f"✅ Deleted category '{category}'")
                else:
                    print("❌ Deletion cancelled")
            else:
                print("❌ Invalid category number")
        
        except ValueError:
            print("❌ Invalid input")

    def main_menu(self):
        """Display main configuration menu"""
        while True:
            print("\n" + "="*50)
            print("⚙️  FILE ORGANIZER - CONFIGURATION SETUP")
            print("="*50)
            
            print("1. 📋 View current configuration")
            print("2. 🎯 Change target directory")
            print("3. ➕ Add new category")
            print("4. ✏️  Modify existing category")
            print("5. 🗑️  Delete category")
            print("6. 💾 Save configuration")
            print("7. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.display_current_config()
            elif choice == "2":
                self.change_target_directory()
            elif choice == "3":
                self.add_category()
            elif choice == "4":
                self.modify_category()
            elif choice == "5":
                self.delete_category()
            elif choice == "6":
                self.save_config()
            elif choice == "7":
                # Auto-save before exit
                save_prompt = input("Save configuration before exit? (y/n): ").lower()
                if save_prompt == 'y':
                    self.save_config()
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
            
            input("\nPress Enter to continue...")

def main():
    print("🗂️  FILE ORGANIZER v1.0 - CONFIGURATION SETUP")
    print("=" * 50)
    
    config_manager = ConfigManager()
    config_manager.main_menu()

if __name__ == "__main__":
    main()