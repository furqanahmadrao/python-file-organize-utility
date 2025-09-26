#!/usr/bin/env python3
"""
Enhanced File Organizer v2.0 - Core Organizer Class
Advanced file organization with multiple features and robust handling
"""

import os
import shutil
import hashlib
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import fnmatch
from dataclasses import dataclass

from .config_manager import ConfigManager, ConfigProfile, OrganizationRule, OrganizeBy
from .logger import Logger, ActionType, LogLevel
from ..utils.cli import CLI, ProgressBar, format_file_size

@dataclass
class FileInfo:
    """Information about a file to be organized"""
    path: Path
    size: int
    modified_time: datetime
    extension: str
    hash: Optional[str] = None
    category: Optional[str] = None
    target_folder: Optional[str] = None
    rule: Optional[OrganizationRule] = None

@dataclass
class OrganizationStats:
    """Statistics for organization operation"""
    total_files: int = 0
    files_moved: int = 0
    files_copied: int = 0
    files_skipped: int = 0
    files_deleted: int = 0
    errors: int = 0
    total_size: int = 0
    categories: Dict[str, int] = None
    duplicates_found: int = 0
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = {}

class FileOrganizer:
    """Enhanced file organizer with advanced features"""
    
    def __init__(self, config_manager: ConfigManager = None, logger: Logger = None):
        self.config_manager = config_manager or ConfigManager()
        self.logger = logger or Logger()
        
        # Operation settings
        self.dry_run = False
        self.progress_callback: Optional[Callable[[int, int], None]] = None
        self.cancel_requested = False
        
        # Threading
        self.max_threads = min(32, (os.cpu_count() or 1) + 4)
        self._lock = threading.Lock()
        
        # File tracking
        self.processed_files: Set[str] = set()
        self.duplicate_hashes: Dict[str, List[Path]] = {}
        
        # Statistics
        self.stats = OrganizationStats()
    
    def organize_directory(self, 
                          target_directory: str = None, 
                          profile_name: str = None,
                          dry_run: bool = False,
                          progress_callback: Callable[[int, int], None] = None,
                          enable_duplicates: bool = False,
                          enable_undo: bool = False) -> OrganizationStats:
        """
        Main method to organize a directory
        
        Args:
            target_directory: Directory to organize (uses profile default if None)
            profile_name: Configuration profile to use (uses current if None)
            dry_run: If True, only simulate the operation
            progress_callback: Callback function for progress updates
            enable_duplicates: If True, detect and handle duplicate files
            enable_undo: If True, create undo information
        
        Returns:
            OrganizationStats: Statistics about the operation
        """
        
        # Setup
        self.dry_run = dry_run
        self.progress_callback = progress_callback
        self.cancel_requested = False
        self.stats = OrganizationStats()
        
        # Get configuration
        if profile_name:
            self.config_manager.set_active_profile(profile_name)
        
        profile = self.config_manager.get_active_profile()
        if not profile:
            CLI.print_error("No active configuration profile")
            return self.stats
        
        # Get target directory
        if target_directory is None:
            target_directory = profile.target_directory
        
        target_path = Path(target_directory)
        if not target_path.exists():
            CLI.print_error(f"Target directory does not exist: {target_directory}")
            return self.stats
        
        # Start logging session
        self.logger.start_session(profile.name, str(target_path))
        
        try:
            CLI.print_header(f"🗂️ FILE ORGANIZER v2.0 - {'PREVIEW MODE' if dry_run else 'ORGANIZING'}")
            CLI.print_info(f"Profile: {profile.name} - {profile.description}")
            CLI.print_info(f"Target: {target_path}")
            CLI.print_info(f"Method: {profile.organize_by.value}")
            
            if not dry_run:
                CLI.print_warning("This will move/modify files. Press Ctrl+C to cancel.")
                time.sleep(2)
            
            # Scan files
            CLI.print_section("📂 Scanning Files")
            file_infos = self._scan_directory(target_path, profile)
            
            if not file_infos:
                CLI.print_info("No files found to organize")
                return self.stats
            
            CLI.print_success(f"Found {len(file_infos)} files to process")
            
            # Detect duplicates if enabled
            if enable_duplicates:
                CLI.print_section("🔍 Detecting Duplicates")
                self._detect_duplicates(file_infos)
                if self.stats.duplicates_found > 0:
                    CLI.print_warning(f"Found {self.stats.duplicates_found} duplicate files")
            
            # Plan organization
            CLI.print_section("📋 Planning Organization")
            self._plan_organization(file_infos, profile)
            
            # Show preview
            if dry_run or not CLI.confirm("Proceed with file organization?", default=True):
                CLI.print_info("Organization cancelled")
                return self.stats
            
            # Execute organization
            CLI.print_section("⚡ Organizing Files")
            self._execute_organization(file_infos, target_path, profile, enable_undo)
            
            # Show results
            self._show_results()
            
        except KeyboardInterrupt:
            CLI.print_warning("Operation cancelled by user")
            self.cancel_requested = True
        except Exception as e:
            CLI.print_error(f"Unexpected error: {e}")
            self.logger.log(ActionType.ERROR, str(target_path), error_message=str(e), level=LogLevel.ERROR)
        finally:
            # End logging session
            session_summary = self.logger.end_session()
            
        return self.stats
    
    def _scan_directory(self, target_path: Path, profile: ConfigProfile) -> List[FileInfo]:
        """Scan directory and collect file information"""
        file_infos = []
        
        try:
            # Get all files
            all_files = []
            for root, dirs, files in os.walk(target_path):
                # Skip hidden directories if not enabled
                if not profile.include_hidden_files:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                # Skip existing organization folders
                dirs[:] = [d for d in dirs if d not in [rule.name for rule in profile.rules]]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip if file is in the same directory as script
                    if file_path.parent == target_path and file_path.suffix in ['.py', '.json', '.log']:
                        continue
                    
                    # Skip hidden files if not enabled
                    if not profile.include_hidden_files and file.startswith('.'):
                        continue
                    
                    # Check exclude patterns
                    if self._should_exclude_file(file_path, profile.exclude_patterns):
                        continue
                    
                    all_files.append(file_path)
            
            # Process files with progress
            if self.progress_callback:
                self.progress_callback(0, len(all_files))
            
            progress_bar = ProgressBar(len(all_files), prefix="Scanning")
            
            for i, file_path in enumerate(all_files):
                if self.cancel_requested:
                    break
                
                try:
                    stat_info = file_path.stat()
                    
                    # Check file size limits
                    if profile.max_file_size and stat_info.st_size > profile.max_file_size:
                        continue
                    
                    file_info = FileInfo(
                        path=file_path,
                        size=stat_info.st_size,
                        modified_time=datetime.fromtimestamp(stat_info.st_mtime),
                        extension=file_path.suffix.lower()
                    )
                    
                    # Get matching rule
                    rule = self.config_manager.get_rule_for_file(file_path, stat_info)
                    if rule:
                        file_info.rule = rule
                        file_info.category = rule.name
                        
                        # Determine target folder
                        target_folder = rule.target_folder or rule.name
                        
                        # Add date-based folder if enabled
                        if profile.create_date_folders:
                            date_folder = file_info.modified_time.strftime("%Y-%m")
                            target_folder = f"{target_folder}/{date_folder}"
                        
                        # Add size-based folder if enabled
                        if profile.create_size_folders:
                            size_folder = self._get_size_category(file_info.size)
                            target_folder = f"{target_folder}/{size_folder}"
                        
                        file_info.target_folder = target_folder
                        file_infos.append(file_info)
                        
                        # Update stats
                        self.stats.total_files += 1
                        self.stats.total_size += file_info.size
                        self.stats.categories[file_info.category] = self.stats.categories.get(file_info.category, 0) + 1
                
                except (OSError, PermissionError) as e:
                    self.logger.log(ActionType.ERROR, str(file_path), error_message=str(e), level=LogLevel.ERROR)
                    self.stats.errors += 1
                
                progress_bar.update()
                if self.progress_callback:
                    self.progress_callback(i + 1, len(all_files))
        
        except Exception as e:
            CLI.print_error(f"Error scanning directory: {e}")
        
        return file_infos
    
    def _should_exclude_file(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if file should be excluded based on patterns"""
        file_name = file_path.name
        
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True
            if fnmatch.fnmatch(str(file_path), pattern):
                return True
        
        return False
    
    def _get_size_category(self, size: int) -> str:
        """Get size category for a file"""
        if size < 1024 * 1024:  # < 1MB
            return "Small"
        elif size < 100 * 1024 * 1024:  # < 100MB
            return "Medium"
        elif size < 1024 * 1024 * 1024:  # < 1GB
            return "Large"
        else:
            return "XLarge"
    
    def _detect_duplicates(self, file_infos: List[FileInfo]):
        """Detect duplicate files based on content hash"""
        hash_map: Dict[str, List[FileInfo]] = {}
        
        progress_bar = ProgressBar(len(file_infos), prefix="Hashing")
        
        def calculate_hash(file_info: FileInfo) -> Optional[str]:
            """Calculate SHA-256 hash of file"""
            try:
                hash_sha256 = hashlib.sha256()
                with open(file_info.path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                return hash_sha256.hexdigest()
            except (OSError, PermissionError):
                return None
        
        # Use threading for hash calculation
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_file = {executor.submit(calculate_hash, file_info): file_info 
                            for file_info in file_infos}
            
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                try:
                    file_hash = future.result()
                    if file_hash:
                        file_info.hash = file_hash
                        if file_hash in hash_map:
                            hash_map[file_hash].append(file_info)
                            self.stats.duplicates_found += 1
                        else:
                            hash_map[file_hash] = [file_info]
                except Exception as e:
                    self.logger.log(ActionType.ERROR, str(file_info.path), 
                                  error_message=f"Hash calculation failed: {e}", level=LogLevel.ERROR)
                
                progress_bar.update()
        
        # Store duplicates for later handling
        self.duplicate_hashes = {hash_val: files for hash_val, files in hash_map.items() if len(files) > 1}
    
    def _plan_organization(self, file_infos: List[FileInfo], profile: ConfigProfile):
        """Plan the organization and show preview"""
        CLI.print_info(f"Organization Plan ({profile.organize_by.value} method):")
        
        # Group by category for display
        category_groups: Dict[str, List[FileInfo]] = {}
        for file_info in file_infos:
            category = file_info.category or "Others"
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(file_info)
        
        # Show plan
        for category, files in category_groups.items():
            total_size = sum(f.size for f in files)
            CLI.print_info(f"  📁 {category}: {len(files)} files ({format_file_size(total_size)})")
            
            # Show first few files as examples
            for file_info in files[:3]:
                target = f"{file_info.target_folder}/{file_info.path.name}"
                CLI.print_file_action("PREVIEW", file_info.path.name, target)
            
            if len(files) > 3:
                CLI.print_info(f"     ... and {len(files) - 3} more files")
    
    def _execute_organization(self, file_infos: List[FileInfo], target_path: Path, 
                            profile: ConfigProfile, enable_undo: bool):
        """Execute the file organization"""
        
        if enable_undo:
            self._create_undo_info(file_infos)
        
        # Create necessary folders
        folders_created = set()
        for file_info in file_infos:
            if file_info.target_folder:
                folder_path = target_path / file_info.target_folder
                if folder_path not in folders_created:
                    if not self.dry_run:
                        folder_path.mkdir(parents=True, exist_ok=True)
                    folders_created.add(folder_path)
        
        if folders_created and not self.dry_run:
            CLI.print_success(f"Created {len(folders_created)} folders")
        
        # Process files
        progress_bar = ProgressBar(len(file_infos), prefix="Processing")
        
        def process_file(file_info: FileInfo) -> bool:
            """Process a single file"""
            if self.cancel_requested:
                return False
            
            try:
                return self._move_file(file_info, target_path, profile)
            except Exception as e:
                self.logger.log(ActionType.ERROR, str(file_info.path), 
                              error_message=str(e), level=LogLevel.ERROR)
                with self._lock:
                    self.stats.errors += 1
                return False
        
        # Use threading for file operations
        with ThreadPoolExecutor(max_workers=min(self.max_threads, 8)) as executor:
            futures = [executor.submit(process_file, file_info) for file_info in file_infos]
            
            for future in as_completed(futures):
                try:
                    success = future.result()
                except Exception as e:
                    CLI.print_error(f"File processing error: {e}")
                    with self._lock:
                        self.stats.errors += 1
                
                progress_bar.update()
                if self.progress_callback:
                    self.progress_callback(progress_bar.current, progress_bar.total)
    
    def _move_file(self, file_info: FileInfo, target_path: Path, profile: ConfigProfile) -> bool:
        """Move a single file to its target location"""
        
        if not file_info.target_folder:
            return False
        
        source_path = file_info.path
        target_folder = target_path / file_info.target_folder
        target_file_path = target_folder / source_path.name
        
        # Handle duplicates
        if target_file_path.exists():
            if profile.handle_duplicates == "skip":
                self.logger.log(ActionType.SKIPPED, str(source_path), str(target_file_path))
                with self._lock:
                    self.stats.files_skipped += 1
                return True
            elif profile.handle_duplicates == "overwrite":
                if not self.dry_run:
                    target_file_path.unlink()
            else:  # rename
                counter = 1
                base_name = target_file_path.stem
                suffix = target_file_path.suffix
                while target_file_path.exists():
                    target_file_path = target_folder / f"{base_name}_{counter}{suffix}"
                    counter += 1
        
        # Perform the move
        try:
            if self.dry_run:
                action_type = ActionType.MOVED
                CLI.print_file_action("PREVIEW", source_path.name, str(target_file_path.relative_to(target_path)))
            else:
                shutil.move(str(source_path), str(target_file_path))
                action_type = ActionType.MOVED
                CLI.print_file_action("MOVED", source_path.name, str(target_file_path.relative_to(target_path)))
            
            # Log the operation
            self.logger.log(
                action_type,
                str(source_path),
                str(target_file_path),
                file_info.size,
                file_info.extension,
                file_info.category
            )
            
            with self._lock:
                self.stats.files_moved += 1
            
            return True
            
        except (OSError, PermissionError, shutil.Error) as e:
            error_msg = f"Failed to move {source_path.name}: {e}"
            CLI.print_error(error_msg)
            self.logger.log(ActionType.ERROR, str(source_path), error_message=str(e), level=LogLevel.ERROR)
            with self._lock:
                self.stats.errors += 1
            return False
    
    def _create_undo_info(self, file_infos: List[FileInfo]):
        """Create undo information for the operation"""
        undo_file = Path("undo_info.json")
        
        undo_data = {
            "timestamp": datetime.now().isoformat(),
            "operations": []
        }
        
        for file_info in file_infos:
            if file_info.target_folder:
                undo_data["operations"].append({
                    "source": str(file_info.path),
                    "target": str(Path(file_info.target_folder) / file_info.path.name),
                    "action": "move"
                })
        
        try:
            import json
            with open(undo_file, 'w') as f:
                json.dump(undo_data, f, indent=2)
            CLI.print_info(f"Undo information saved to {undo_file}")
        except Exception as e:
            CLI.print_warning(f"Could not save undo information: {e}")
    
    def _show_results(self):
        """Display organization results"""
        CLI.print_header("🎉 ORGANIZATION COMPLETE")
        
        if self.dry_run:
            CLI.print_info("This was a preview. No files were actually moved.")
        
        CLI.print_statistics(self.stats.categories)
        
        # Summary
        CLI.print_section("📊 Summary")
        CLI.print_success(f"Total files processed: {self.stats.total_files}")
        CLI.print_success(f"Files moved: {self.stats.files_moved}")
        
        if self.stats.files_skipped > 0:
            CLI.print_warning(f"Files skipped: {self.stats.files_skipped}")
        
        if self.stats.errors > 0:
            CLI.print_error(f"Errors encountered: {self.stats.errors}")
        
        if self.stats.duplicates_found > 0:
            CLI.print_info(f"Duplicate files found: {self.stats.duplicates_found}")
        
        CLI.print_info(f"Total size processed: {format_file_size(self.stats.total_size)}")
    
    def cancel_operation(self):
        """Cancel the current operation"""
        self.cancel_requested = True
    
    def undo_last_operation(self, undo_file: str = "undo_info.json") -> bool:
        """Undo the last organization operation"""
        try:
            import json
            
            undo_path = Path(undo_file)
            if not undo_path.exists():
                CLI.print_error("No undo information found")
                return False
            
            with open(undo_path, 'r') as f:
                undo_data = json.load(f)
            
            operations = undo_data.get("operations", [])
            if not operations:
                CLI.print_error("No operations to undo")
                return False
            
            CLI.print_info(f"Undoing {len(operations)} operations from {undo_data['timestamp']}")
            
            success_count = 0
            error_count = 0
            
            progress_bar = ProgressBar(len(operations), prefix="Undoing")
            
            for op in operations:
                try:
                    target_path = Path(op["target"])
                    source_path = Path(op["source"])
                    
                    if target_path.exists():
                        # Restore original directory structure if needed
                        source_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(target_path), str(source_path))
                        success_count += 1
                        CLI.print_file_action("RESTORED", target_path.name, str(source_path))
                    
                except Exception as e:
                    CLI.print_error(f"Failed to undo {op['target']}: {e}")
                    error_count += 1
                
                progress_bar.update()
            
            CLI.print_success(f"Undo complete: {success_count} operations restored")
            if error_count > 0:
                CLI.print_warning(f"Undo errors: {error_count}")
            
            # Remove undo file after successful undo
            if error_count == 0:
                undo_path.unlink()
                CLI.print_info("Undo information file removed")
            
            return error_count == 0
            
        except Exception as e:
            CLI.print_error(f"Undo failed: {e}")
            return False