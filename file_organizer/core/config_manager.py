#!/usr/bin/env python3
"""
Enhanced Configuration Manager for File Organizer v2.0
Supports multiple profiles, advanced rules, and import/export functionality
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class OrganizeBy(Enum):
    """Different organization methods"""
    EXTENSION = "extension"
    SIZE = "size"
    DATE = "date"
    MIXED = "mixed"

@dataclass
class OrganizationRule:
    """A single organization rule"""
    name: str
    extensions: List[str]
    size_min: Optional[int] = None  # In bytes
    size_max: Optional[int] = None  # In bytes
    date_min: Optional[str] = None  # ISO format
    date_max: Optional[str] = None  # ISO format
    target_folder: Optional[str] = None
    enabled: bool = True

@dataclass
class ConfigProfile:
    """Configuration profile for different use cases"""
    name: str
    description: str
    target_directory: str
    organize_by: OrganizeBy
    rules: List[OrganizationRule]
    create_date_folders: bool = False
    create_size_folders: bool = False
    handle_duplicates: str = "rename"  # rename, skip, overwrite
    preserve_structure: bool = False
    exclude_patterns: List[str] = None
    include_hidden_files: bool = False
    max_file_size: Optional[int] = None  # In bytes
    created_date: str = ""
    last_modified: str = ""

    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = []
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()

class ConfigManager:
    """Enhanced configuration manager with profiles and advanced rules"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.current_profile: Optional[ConfigProfile] = None
        self.profiles: Dict[str, ConfigProfile] = {}
        
        # Load existing profiles
        self.load_all_profiles()
        
        # Create default profile if none exist
        if not self.profiles:
            self.create_default_profile()
    
    def create_default_profile(self) -> ConfigProfile:
        """Create and save default configuration profile"""
        default_rules = [
            OrganizationRule(
                name="Images",
                extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", 
                          ".tiff", ".tif", ".raw", ".cr2", ".nef", ".arw", ".dng"]
            ),
            OrganizationRule(
                name="Documents",
                extensions=[".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", 
                          ".ppt", ".pptx", ".csv", ".md", ".tex", ".epub", ".mobi"]
            ),
            OrganizationRule(
                name="Videos",
                extensions=[".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", 
                          ".mpg", ".mpeg", ".3gp", ".f4v", ".asf", ".rm", ".rmvb"]
            ),
            OrganizationRule(
                name="Audio",
                extensions=[".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus", 
                          ".ape", ".ac3", ".dts", ".amr", ".au"]
            ),
            OrganizationRule(
                name="Archives",
                extensions=[".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".lz", 
                          ".lzma", ".cab", ".deb", ".rpm", ".dmg", ".iso"]
            ),
            OrganizationRule(
                name="Code",
                extensions=[".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", 
                          ".rb", ".go", ".rs", ".ts", ".jsx", ".vue", ".swift", ".kt", ".cs"]
            ),
            OrganizationRule(
                name="Executables",
                extensions=[".exe", ".msi", ".app", ".deb", ".rpm", ".dmg", ".pkg", ".run", ".bin"]
            ),
            OrganizationRule(
                name="Fonts",
                extensions=[".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".fnt"]
            ),
            OrganizationRule(
                name="Others",
                extensions=[],  # Catch-all for unknown extensions
            )
        ]
        
        profile = ConfigProfile(
            name="default",
            description="Default file organization profile",
            target_directory=str(Path.home() / "Downloads"),
            organize_by=OrganizeBy.EXTENSION,
            rules=default_rules,
            exclude_patterns=[".DS_Store", "Thumbs.db", "desktop.ini", "*.tmp", "*.temp"]
        )
        
        self.profiles["default"] = profile
        self.current_profile = profile
        self.save_profile(profile)
        
        return profile
    
    def create_profile_for_use_case(self, use_case: str) -> ConfigProfile:
        """Create specialized profiles for different use cases"""
        
        if use_case == "photographer":
            return self._create_photographer_profile()
        elif use_case == "developer":
            return self._create_developer_profile()
        elif use_case == "student":
            return self._create_student_profile()
        elif use_case == "business":
            return self._create_business_profile()
        else:
            return self.create_default_profile()
    
    def _create_photographer_profile(self) -> ConfigProfile:
        """Profile optimized for photographers"""
        rules = [
            OrganizationRule(
                name="RAW_Images",
                extensions=[".raw", ".cr2", ".nef", ".arw", ".dng", ".raf", ".orf", ".rw2"],
                target_folder="RAW"
            ),
            OrganizationRule(
                name="JPEG_Images",
                extensions=[".jpg", ".jpeg"],
                target_folder="JPEG"
            ),
            OrganizationRule(
                name="PNG_Images", 
                extensions=[".png", ".tiff", ".tif"],
                target_folder="PNG_TIFF"
            ),
            OrganizationRule(
                name="Videos",
                extensions=[".mp4", ".mov", ".avi", ".mkv"],
                target_folder="Videos"
            ),
            OrganizationRule(
                name="Large_Files",
                extensions=[],
                size_min=100 * 1024 * 1024,  # 100MB+
                target_folder="Large_Files"
            )
        ]
        
        profile = ConfigProfile(
            name="photographer",
            description="Optimized for photographers and visual content creators",
            target_directory=str(Path.home() / "Pictures"),
            organize_by=OrganizeBy.MIXED,
            rules=rules,
            create_date_folders=True,
            create_size_folders=True
        )
        
        return profile
    
    def _create_developer_profile(self) -> ConfigProfile:
        """Profile optimized for developers"""
        rules = [
            OrganizationRule(
                name="Python",
                extensions=[".py", ".pyx", ".pyw", ".pyi"],
                target_folder="Python"
            ),
            OrganizationRule(
                name="Web",
                extensions=[".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".vue", ".scss", ".sass"],
                target_folder="Web"
            ),
            OrganizationRule(
                name="Config",
                extensions=[".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf"],
                target_folder="Config"
            ),
            OrganizationRule(
                name="Documentation",
                extensions=[".md", ".rst", ".txt", ".doc", ".docx", ".pdf"],
                target_folder="Docs"
            ),
            OrganizationRule(
                name="Archives",
                extensions=[".zip", ".tar", ".gz", ".bz2", ".7z"],
                target_folder="Archives"
            ),
            OrganizationRule(
                name="Executables",
                extensions=[".exe", ".msi", ".app", ".deb", ".rpm"],
                target_folder="Executables"
            )
        ]
        
        profile = ConfigProfile(
            name="developer",
            description="Optimized for software developers and programmers",
            target_directory=str(Path.home() / "Downloads"),
            organize_by=OrganizeBy.EXTENSION,
            rules=rules,
            exclude_patterns=[".git", ".vscode", "__pycache__", "node_modules", "*.pyc"]
        )
        
        return profile
    
    def _create_student_profile(self) -> ConfigProfile:
        """Profile optimized for students"""
        rules = [
            OrganizationRule(
                name="Textbooks",
                extensions=[".pdf"],
                size_min=10 * 1024 * 1024,  # 10MB+ PDFs are likely textbooks
                target_folder="Textbooks"
            ),
            OrganizationRule(
                name="Assignments",
                extensions=[".doc", ".docx", ".txt", ".rtf"],
                target_folder="Assignments"
            ),
            OrganizationRule(
                name="Spreadsheets",
                extensions=[".xls", ".xlsx", ".csv"],
                target_folder="Spreadsheets"
            ),
            OrganizationRule(
                name="Presentations",
                extensions=[".ppt", ".pptx"],
                target_folder="Presentations"
            ),
            OrganizationRule(
                name="Images",
                extensions=[".jpg", ".png", ".gif", ".bmp"],
                target_folder="Images"
            ),
            OrganizationRule(
                name="Archives",
                extensions=[".zip", ".rar", ".7z"],
                target_folder="Archives"
            )
        ]
        
        profile = ConfigProfile(
            name="student",
            description="Optimized for students and academic work",
            target_directory=str(Path.home() / "Documents"),
            organize_by=OrganizeBy.MIXED,
            rules=rules,
            create_date_folders=True
        )
        
        return profile
    
    def _create_business_profile(self) -> ConfigProfile:
        """Profile optimized for business users"""
        rules = [
            OrganizationRule(
                name="Contracts",
                extensions=[".pdf", ".doc", ".docx"],
                target_folder="Legal_Documents"
            ),
            OrganizationRule(
                name="Spreadsheets",
                extensions=[".xls", ".xlsx", ".csv"],
                target_folder="Financial_Data"
            ),
            OrganizationRule(
                name="Presentations",
                extensions=[".ppt", ".pptx"],
                target_folder="Presentations"
            ),
            OrganizationRule(
                name="Images",
                extensions=[".jpg", ".png", ".gif"],
                target_folder="Marketing_Assets"
            ),
            OrganizationRule(
                name="Archives",
                extensions=[".zip", ".rar"],
                target_folder="Archives"
            )
        ]
        
        profile = ConfigProfile(
            name="business",
            description="Optimized for business and professional use",
            target_directory=str(Path.home() / "Documents" / "Business"),
            organize_by=OrganizeBy.EXTENSION,
            rules=rules,
            create_date_folders=True,
            preserve_structure=True
        )
        
        return profile
    
    def save_profile(self, profile: ConfigProfile) -> bool:
        """Save a configuration profile to file"""
        try:
            profile.last_modified = datetime.now().isoformat()
            
            profile_path = self.config_dir / f"{profile.name}.json"
            
            # Convert to dictionary for JSON serialization
            profile_dict = asdict(profile)
            # Convert enum to string for JSON serialization
            profile_dict['organize_by'] = profile.organize_by.value
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_dict, f, indent=4, ensure_ascii=False)
            
            self.profiles[profile.name] = profile
            return True
            
        except Exception as e:
            print(f"Error saving profile '{profile.name}': {e}")
            return False
    
    def load_profile(self, profile_name: str) -> Optional[ConfigProfile]:
        """Load a configuration profile from file"""
        try:
            profile_path = self.config_dir / f"{profile_name}.json"
            
            if not profile_path.exists():
                return None
            
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_dict = json.load(f)
            
            # Convert rules back to OrganizationRule objects
            rules = []
            for rule_data in profile_dict.get('rules', []):
                rule = OrganizationRule(**rule_data)
                rules.append(rule)
            
            profile_dict['rules'] = rules
            
            # Convert organize_by back to enum
            if 'organize_by' in profile_dict:
                profile_dict['organize_by'] = OrganizeBy(profile_dict['organize_by'])
            
            profile = ConfigProfile(**profile_dict)
            self.profiles[profile.name] = profile
            
            return profile
            
        except Exception as e:
            print(f"Error loading profile '{profile_name}': {e}")
            return None
    
    def load_all_profiles(self):
        """Load all available configuration profiles"""
        if not self.config_dir.exists():
            return
        
        for profile_file in self.config_dir.glob("*.json"):
            profile_name = profile_file.stem
            self.load_profile(profile_name)
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a configuration profile"""
        if profile_name == "default":
            return False  # Cannot delete default profile
        
        try:
            profile_path = self.config_dir / f"{profile_name}.json"
            if profile_path.exists():
                profile_path.unlink()
            
            if profile_name in self.profiles:
                del self.profiles[profile_name]
            
            # Switch to default if current profile was deleted
            if self.current_profile and self.current_profile.name == profile_name:
                self.current_profile = self.profiles.get("default")
            
            return True
            
        except Exception as e:
            print(f"Error deleting profile '{profile_name}': {e}")
            return False
    
    def export_profile(self, profile_name: str, export_path: str) -> bool:
        """Export a profile to a file"""
        if profile_name not in self.profiles:
            return False
        
        try:
            profile = self.profiles[profile_name]
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(profile), f, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting profile '{profile_name}': {e}")
            return False
    
    def import_profile(self, import_path: str, new_name: Optional[str] = None) -> bool:
        """Import a profile from a file with optional renaming"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                profile_dict = json.load(f)
            
            # Convert rules back to OrganizationRule objects
            rules = []
            for rule_data in profile_dict.get('rules', []):
                rule = OrganizationRule(**rule_data)
                rules.append(rule)
            
            profile_dict['rules'] = rules
            
            # Convert organize_by back to enum
            if 'organize_by' in profile_dict:
                profile_dict['organize_by'] = OrganizeBy(profile_dict['organize_by'])
            
            # Rename profile if new name provided
            if new_name:
                profile_dict['name'] = new_name
            
            profile = ConfigProfile(**profile_dict)
            
            # Save the imported profile
            return self.save_profile(profile)
            
        except Exception as e:
            print(f"Error importing profile from '{import_path}': {e}")
            return False
    
    def get_profile_list(self) -> List[str]:
        """Get list of available profile names"""
        return list(self.profiles.keys())
    
    def set_active_profile(self, profile_name: str) -> bool:
        """Set the active configuration profile"""
        if profile_name in self.profiles:
            self.current_profile = self.profiles[profile_name]
            return True
        return False
    
    def get_active_profile(self) -> Optional[ConfigProfile]:
        """Get the currently active configuration profile"""
        return self.current_profile
    
    def get_profile(self, profile_name: str) -> Optional[ConfigProfile]:
        """Get a specific profile by name"""
        return self.profiles.get(profile_name)
    
    def validate_profile(self, profile: ConfigProfile) -> tuple[bool, List[str]]:
        """Validate a configuration profile and return (is_valid, issues)"""
        issues = []
        
        # Check if target directory exists or can be created
        target_path = Path(profile.target_directory)
        if not target_path.exists():
            try:
                target_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create target directory: {e}")
        
        # Check for duplicate rule names
        rule_names = [rule.name for rule in profile.rules]
        duplicates = set([name for name in rule_names if rule_names.count(name) > 1])
        if duplicates:
            issues.append(f"Duplicate rule names: {', '.join(duplicates)}")
        
        # Check for conflicting extensions
        extension_rules = {}
        for rule in profile.rules:
            for ext in rule.extensions:
                if ext in extension_rules:
                    issues.append(f"Extension {ext} is used in both '{rule.name}' and '{extension_rules[ext]}' rules")
                else:
                    extension_rules[ext] = rule.name
        
        # Check for empty rules
        if not profile.rules:
            issues.append("Profile has no organization rules")
        
        # Check for valid organize_by value
        if not isinstance(profile.organize_by, OrganizeBy):
            issues.append("Invalid organization method")
        
        return len(issues) == 0, issues
    
    def get_rule_for_file(self, file_path: Path, file_stats: os.stat_result = None) -> Optional[OrganizationRule]:
        """Get the appropriate rule for a given file"""
        if not self.current_profile:
            return None
        
        file_ext = file_path.suffix.lower()
        file_size = file_stats.st_size if file_stats else file_path.stat().st_size
        file_mtime = datetime.fromtimestamp(file_stats.st_mtime if file_stats else file_path.stat().st_mtime)
        
        # Check each rule
        for rule in self.current_profile.rules:
            if not rule.enabled:
                continue
            
            # Check extension match
            if rule.extensions and file_ext not in [ext.lower() for ext in rule.extensions]:
                continue
            
            # Check size constraints
            if rule.size_min is not None and file_size < rule.size_min:
                continue
            if rule.size_max is not None and file_size > rule.size_max:
                continue
            
            # Check date constraints
            if rule.date_min is not None:
                min_date = datetime.fromisoformat(rule.date_min)
                if file_mtime < min_date:
                    continue
            if rule.date_max is not None:
                max_date = datetime.fromisoformat(rule.date_max)
                if file_mtime > max_date:
                    continue
            
            return rule
        
        # Return "Others" rule if no specific rule matches
        for rule in self.current_profile.rules:
            if rule.name == "Others" and rule.enabled:
                return rule
        
        return None