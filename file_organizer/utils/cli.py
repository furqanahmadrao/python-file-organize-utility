#!/usr/bin/env python3
"""
Enhanced CLI Interface for File Organizer v2.0
Provides colored output, progress bars, and better user experience
"""

import sys
import os
import shutil
from enum import Enum
from typing import Optional

class Colors:
    """ANSI color codes for terminal output"""
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    
    @classmethod
    def disable(cls):
        """Disable colors for non-terminal output"""
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, '')

# Disable colors on Windows if not supported or redirected output
if os.name == 'nt' or not sys.stdout.isatty():
    # Keep colors on Windows Terminal and VS Code terminal
    if not (os.environ.get('WT_SESSION') or os.environ.get('TERM_PROGRAM')):
        Colors.disable()

class Icons:
    """Unicode icons for better visual representation"""
    
    # Status icons
    SUCCESS = '✅'
    ERROR = '❌'
    WARNING = '⚠️'
    INFO = 'ℹ️'
    
    # File type icons
    FOLDER = '📁'
    FILE = '📄'
    IMAGE = '🖼️'
    DOCUMENT = '📋'
    VIDEO = '🎥'
    AUDIO = '🎵'
    ARCHIVE = '📦'
    CODE = '💻'
    
    # Action icons
    MOVE = '➡️'
    COPY = '📋'
    DELETE = '🗑️'
    PREVIEW = '👀'
    CONFIG = '⚙️'
    LOG = '📊'
    SEARCH = '🔍'
    
    # Progress icons
    PROCESSING = '⚡'
    COMPLETED = '🎉'
    SKIPPED = '⏭️'

class ProgressBar:
    """Simple progress bar for terminal"""
    
    def __init__(self, total: int, width: int = 50, prefix: str = "Progress"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
        
    def update(self, increment: int = 1):
        """Update progress bar"""
        self.current += increment
        if self.current > self.total:
            self.current = self.total
            
        # Calculate progress
        progress = self.current / self.total if self.total > 0 else 0
        filled_width = int(self.width * progress)
        
        # Create bar
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        percentage = progress * 100
        
        # Print progress
        print(f'\r{self.prefix}: [{bar}] {percentage:.1f}% ({self.current}/{self.total})', 
              end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete

class CLI:
    """Enhanced CLI interface with colors and formatting"""
    
    @staticmethod
    def print_header(text: str):
        """Print a formatted header"""
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_BLUE}{'='*60}{Colors.RESET}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"{Colors.BRIGHT_GREEN}{Icons.SUCCESS} {message}{Colors.RESET}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"{Colors.BRIGHT_RED}{Icons.ERROR} {message}{Colors.RESET}")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(f"{Colors.BRIGHT_YELLOW}{Icons.WARNING} {message}{Colors.RESET}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"{Colors.BRIGHT_CYAN}{Icons.INFO} {message}{Colors.RESET}")
    
    @staticmethod
    def print_section(title: str):
        """Print a section header"""
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_MAGENTA}{Icons.FOLDER} {title}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * (len(title) + 3)}{Colors.RESET}")
    
    @staticmethod
    def print_file_action(action: str, filename: str, destination: str = None):
        """Print file action with appropriate icon"""
        if action == "MOVED":
            icon = Icons.MOVE
            color = Colors.BRIGHT_GREEN
        elif action == "COPIED":
            icon = Icons.COPY
            color = Colors.BRIGHT_BLUE
        elif action == "DELETED":
            icon = Icons.DELETE
            color = Colors.BRIGHT_RED
        elif action == "SKIPPED":
            icon = Icons.SKIPPED
            color = Colors.BRIGHT_YELLOW
        else:
            icon = Icons.FILE
            color = Colors.WHITE
        
        if destination:
            print(f"  {color}{icon} {filename} → {destination}{Colors.RESET}")
        else:
            print(f"  {color}{icon} {filename}{Colors.RESET}")
    
    @staticmethod
    def print_statistics(stats: dict):
        """Print organized statistics"""
        CLI.print_section("📊 ORGANIZATION STATISTICS")
        
        total_files = sum(stats.values())
        
        if total_files == 0:
            CLI.print_info("No files were processed")
            return
        
        # Sort categories by count
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        
        for category, count in sorted_stats:
            if count > 0:
                percentage = (count / total_files) * 100
                bar_width = int(20 * (count / max(stats.values())))
                bar = '█' * bar_width + '░' * (20 - bar_width)
                
                print(f"  {CLI._get_category_icon(category)} {category:.<15} "
                      f"[{bar}] {count:>3} files ({percentage:>5.1f}%)")
        
        print(f"\n  {Colors.BOLD}Total Files Processed: {total_files}{Colors.RESET}")
    
    @staticmethod
    def _get_category_icon(category: str) -> str:
        """Get icon for file category"""
        category_icons = {
            'Images': Icons.IMAGE,
            'Documents': Icons.DOCUMENT,
            'Videos': Icons.VIDEO,
            'Audio': Icons.AUDIO,
            'Archives': Icons.ARCHIVE,
            'Code': Icons.CODE,
            'Others': Icons.FILE
        }
        return category_icons.get(category, Icons.FILE)
    
    @staticmethod
    def confirm(message: str, default: bool = False) -> bool:
        """Get user confirmation"""
        default_text = "Y/n" if default else "y/N"
        response = input(f"{Colors.BRIGHT_YELLOW}❓ {message} ({default_text}): {Colors.RESET}")
        
        if not response.strip():
            return default
        
        return response.lower().startswith('y')
    
    @staticmethod
    def select_option(prompt: str, options: list) -> int:
        """Display options and get user selection"""
        print(f"\n{Colors.BRIGHT_CYAN}❓ {prompt}{Colors.RESET}")
        
        for i, option in enumerate(options, 1):
            print(f"  {Colors.BRIGHT_WHITE}{i}.{Colors.RESET} {option}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BRIGHT_YELLOW}Enter choice (1-{len(options)}): {Colors.RESET}")
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1
                else:
                    CLI.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                CLI.print_error("Please enter a valid number")
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_logo():
        """Print application logo"""
        logo = f"""
{Colors.BRIGHT_BLUE}{Colors.BOLD}
 ███████╗██╗██╗     ███████╗     ██████╗ ██████╗  ██████╗  █████╗ ███╗   ██╗██╗███████╗███████╗██████╗ 
 ██╔════╝██║██║     ██╔════╝    ██╔═══██╗██╔══██╗██╔════╝ ██╔══██╗████╗  ██║██║╚══███╔╝██╔════╝██╔══██╗
 █████╗  ██║██║     █████╗      ██║   ██║██████╔╝██║  ███╗███████║██╔██╗ ██║██║  ███╔╝ █████╗  ██████╔╝
 ██╔══╝  ██║██║     ██╔══╝      ██║   ██║██╔══██╗██║   ██║██╔══██║██║╚██╗██║██║ ███╔╝  ██╔══╝  ██╔══██╗
 ██║     ██║███████╗███████╗    ╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚████║██║███████╗███████╗██║  ██║
 ╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.BRIGHT_CYAN}                                    Professional File Organization Utility v2.0{Colors.RESET}
{Colors.DIM}                                         Transform chaos into order with style{Colors.RESET}
"""
        print(logo)
    
    @staticmethod
    def create_progress_bar(total: int, description: str = ""):
        """Create a simple progress bar"""
        class SimpleProgressBar:
            def __init__(self, total, desc):
                self.total = total
                self.current = 0
                self.desc = desc
                
            def update(self, value):
                self.current = value
                percent = (value / self.total * 100) if self.total > 0 else 0
                bar_length = 30
                filled = int(bar_length * value / self.total) if self.total > 0 else 0
                bar = "█" * filled + "░" * (bar_length - filled)
                print(f"\r{self.desc}: [{bar}] {percent:5.1f}%", end="", flush=True)
                
            def finish(self):
                print()  # New line when done
                
        return SimpleProgressBar(total, description)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def get_terminal_width() -> int:
    """Get terminal width"""
    return shutil.get_terminal_size((80, 24)).columns

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to fit terminal width"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."