#!/usr/bin/env python3
"""
FileNest - Professional File Organizer
Core organizer module that follows the exact specification for production use.
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional, Tuple

class FileOrganizer:
    """Core file organization engine following the specification."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.setup_logging()
        
        # Statistics
        self.moved_count = 0
        self.skipped_count = 0
        self.error_count = 0
        
    def load_config(self) -> Dict:
        """Load configuration from config.json"""
        try:
            if not os.path.exists(self.config_path):
                self.create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate and set defaults
            if 'target_path' not in config:
                config['target_path'] = self.get_default_downloads_path()
            
            if 'categories' not in config:
                config['categories'] = self.get_default_categories()
            
            if 'others_folder' not in config:
                config['others_folder'] = "Others"
            
            if 'duplicate_strategy' not in config:
                config['duplicate_strategy'] = "rename"
                
            if 'move_empty_folders' not in config:
                config['move_empty_folders'] = False
            
            return config
            
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Creating default configuration...")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration file"""
        default_config = {
            "target_path": self.get_default_downloads_path(),
            "categories": self.get_default_categories(),
            "others_folder": "Others",
            "move_empty_folders": False,
            "duplicate_strategy": "rename"
        }
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config: {self.config_path}")
        except Exception as e:
            print(f"Error creating config: {e}")
        
        return default_config
    
    def get_default_downloads_path(self) -> str:
        """Get platform-appropriate default downloads path"""
        if os.name == 'nt':  # Windows
            return str(Path.home() / "Downloads")
        else:  # macOS/Linux
            return str(Path.home() / "Downloads")
    
    def get_default_categories(self) -> Dict[str, List[str]]:
        """Get default file categories"""
        return {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Software": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".appimage"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb", ".go", ".rs"]
        }
    
    def setup_logging(self):
        """Setup logging to log.txt with ISO timestamp format"""
        log_format = '%(asctime)s | %(message)s'
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler('log.txt', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Remove default timestamp and use custom format
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setFormatter(logging.Formatter(log_format, date_format))
    
    def determine_category(self, file_path: Path) -> str:
        """Determine which category a file belongs to based on extension"""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.config['categories'].items():
            if extension in [ext.lower() for ext in extensions]:
                return category
        
        return self.config['others_folder']
    
    def generate_unique_filename(self, dest_path: Path) -> Path:
        """Generate unique filename if file already exists"""
        if not dest_path.exists():
            return dest_path
        
        strategy = self.config.get('duplicate_strategy', 'rename')
        
        if strategy == 'skip':
            return None  # Signal to skip
        elif strategy == 'overwrite':
            return dest_path
        else:  # rename (default)
            base = dest_path.stem
            suffix = dest_path.suffix
            parent = dest_path.parent
            counter = 1
            
            while True:
                new_name = f"{base} ({counter}){suffix}"
                new_path = parent / new_name
                if not new_path.exists():
                    return new_path
                counter += 1
    
    def move_file(self, source: Path, dest_dir: Path, dry_run: bool = False) -> Tuple[bool, str]:
        """Move a file to the destination directory with error handling"""
        try:
            # Create destination directory if it doesn't exist
            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_dir / source.name
            unique_dest = self.generate_unique_filename(dest_path)
            
            if unique_dest is None:  # Skip strategy
                return False, "Skipped: File exists and duplicate_strategy is 'skip'"
            
            if dry_run:
                action = "Would move" if unique_dest == dest_path else f"Would move (rename to {unique_dest.name})"
                return True, action
            
            # Perform the actual move
            final_dest = shutil.move(str(source), str(unique_dest))
            
            # Preserve original timestamps
            try:
                stat_info = source.stat() if source.exists() else None
                if stat_info:
                    os.utime(final_dest, (stat_info.st_atime, stat_info.st_mtime))
            except Exception:
                pass  # Not critical if timestamp preservation fails
            
            action = "Moved" if unique_dest == dest_path else f"Moved (renamed to {Path(final_dest).name})"
            return True, action
            
        except PermissionError:
            return False, "Error: Permission denied"
        except OSError as e:
            return False, f"Error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def log_action(self, action: str, filename: str, source_path: str, dest_path: str = "", error: str = ""):
        """Log action to log.txt with specified format"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        if error:
            message = f"{action} | {filename} | {source_path} | {error}"
        elif dest_path:
            message = f"{action} | {filename} | {source_path} | {dest_path}"
        else:
            message = f"{action} | {filename} | {source_path}"
        
        # Write directly to log file with custom format
        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} | {message}\n")
        except Exception:
            pass  # Don't fail if logging fails
    
    def organize_once(self, target_path: Optional[str] = None, dry_run: bool = False) -> Dict[str, int]:
        """Organize files once - core functionality"""
        # Use provided path or config path
        path_to_organize = Path(target_path) if target_path else Path(self.config['target_path'])
        
        if not path_to_organize.exists():
            print(f"Error: Target path does not exist: {path_to_organize}")
            return {"moved": 0, "skipped": 0, "errors": 1}
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Organizing: {path_to_organize}")
        
        # Reset statistics
        self.moved_count = 0
        self.skipped_count = 0  
        self.error_count = 0
        
        # Process files in the directory
        for item in path_to_organize.iterdir():
            # Skip hidden files and directories
            if item.name.startswith('.') or item.is_dir():
                if item.name.startswith('.'):
                    self.log_action("Skipped", item.name, str(item), "", "Reason: hidden file")
                    self.skipped_count += 1
                continue
            
            # Determine category and destination
            category = self.determine_category(item)
            dest_dir = path_to_organize / category
            
            # Move the file
            success, message = self.move_file(item, dest_dir, dry_run)
            
            if success:
                self.moved_count += 1
                if not dry_run:
                    self.log_action("Moved", item.name, str(item), str(dest_dir / item.name))
                else:
                    print(f"  {message}: {item.name} -> {category}/")
            else:
                self.error_count += 1
                self.log_action("Error", item.name, str(item), "", message)
                if not dry_run:
                    print(f"  Error: {item.name} - {message}")
        
        return {
            "moved": self.moved_count,
            "skipped": self.skipped_count,
            "errors": self.error_count
        }
    
    def start_watcher(self, target_path: Optional[str] = None):
        """Start real-time file watcher using watchdog"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
        except ImportError:
            print("Error: watchdog library not installed.")
            print("Install it with: pip install watchdog")
            return
        
        path_to_watch = target_path if target_path else self.config['target_path']
        
        class FileHandler(FileSystemEventHandler):
            def __init__(self, organizer):
                self.organizer = organizer
            
            def on_created(self, event):
                if not event.is_directory:
                    file_path = Path(event.src_path)
                    if not file_path.name.startswith('.'):
                        print(f"New file detected: {file_path.name}")
                        
                        # Organize just this file
                        category = self.organizer.determine_category(file_path)
                        dest_dir = file_path.parent / category
                        
                        success, message = self.organizer.move_file(file_path, dest_dir)
                        
                        if success:
                            self.organizer.log_action("Moved", file_path.name, str(file_path), str(dest_dir / file_path.name))
                            print(f"  Moved to: {category}/")
                        else:
                            self.organizer.log_action("Error", file_path.name, str(file_path), "", message)
                            print(f"  Error: {message}")
        
        event_handler = FileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path_to_watch, recursive=False)
        observer.start()
        
        print(f"Watching for new files in: {path_to_watch}")
        print("Press Ctrl+C to stop...")
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nFile watcher stopped.")
        
        observer.join()

def show_recent_logs(num_entries: int = 50, errors_only: bool = False):
    """Show recent log entries"""
    try:
        if not os.path.exists('log.txt'):
            print("No log file found.")
            return
        
        with open('log.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter errors if requested
        if errors_only:
            lines = [line for line in lines if 'Error' in line]
        
        # Get last N entries
        recent_lines = lines[-num_entries:] if len(lines) > num_entries else lines
        
        print(f"\n--- Recent Log Entries (Last {len(recent_lines)}) ---")
        for line in recent_lines:
            print(line.strip())
        
    except Exception as e:
        print(f"Error reading log: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='organize',
        description='FileNest (organize) v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  organize                    # Organize default folder once
  organize --dry-run          # Preview what would be moved
  organize --path ~/Desktop   # Organize specific folder
  organize --watch            # Start real-time monitoring
  organize --show-log         # Show recent log entries
        """
    )
    
    parser.add_argument('--path', type=str, help='Run on PATH instead of config target_path')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be moved (no changes)')
    parser.add_argument('--show-log', action='store_true', help='Print last 50 log entries')
    parser.add_argument('--watch', action='store_true', help='Run real-time monitor (requires watchdog)')
    parser.add_argument('--once', action='store_true', help='Run once and exit (default)')
    parser.add_argument('--version', action='version', version='FileNest v2.0')
    parser.add_argument('--errors-only', action='store_true', help='Show only error log entries')
    parser.add_argument('--log-entries', type=int, default=50, help='Number of log entries to show')
    
    args = parser.parse_args()
    
    # Handle log viewing
    if args.show_log:
        show_recent_logs(args.log_entries, args.errors_only)
        return
    
    # Create organizer instance
    organizer = FileOrganizer()
    
    # Handle different modes
    if args.watch:
        organizer.start_watcher(args.path)
    else:
        # Run once (default behavior)
        stats = organizer.organize_once(args.path, args.dry_run)
        
        # Print summary
        print(f"\n--- Summary ---")
        print(f"Files moved: {stats['moved']}")
        print(f"Files skipped: {stats['skipped']}")
        print(f"Errors: {stats['errors']}")
        
        if not args.dry_run and stats['moved'] > 0:
            print(f"Check log.txt for detailed information")

if __name__ == "__main__":
    main()