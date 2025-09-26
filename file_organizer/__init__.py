"""
File Organizer v2.0 - Professional File Organization Utility
A comprehensive tool for organizing files with advanced features.
"""

__version__ = "2.0.0"
__author__ = "Furqan Ahmad Rao"
__email__ = "furqanrao091@gmail.com"
__description__ = "Professional file organization utility with advanced features"

from .core.organizer import FileOrganizer
from .core.config_manager import ConfigManager
from .core.logger import Logger

__all__ = ['FileOrganizer', 'ConfigManager', 'Logger']