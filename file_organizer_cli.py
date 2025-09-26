#!/usr/bin/env python3
"""
Enhanced CLI Application for File Organizer v2.0
Feature-rich command-line interface with advanced functionality
"""

import sys
import os
import argparse
import signal
from pathlib import Path
from typing import Optional

# Add the package to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from file_organizer.core.organizer import FileOrganizer
from file_organizer.core.config_manager import ConfigManager, OrganizeBy
from file_organizer.core.logger import Logger
from file_organizer.utils.cli import CLI, Colors, Icons

class EnhancedCLI:
    """Enhanced CLI application with advanced features"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = Logger()
        self.organizer = FileOrganizer(self.config_manager, self.logger)
        self.interrupted = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interruption signals"""
        if not self.interrupted:
            CLI.print_warning("\nOperation interrupted. Cleaning up...")
            self.organizer.cancel_operation()
            self.interrupted = True
        else:
            CLI.print_error("\nForce quit!")
            sys.exit(1)
    
    def run(self):
        """Main application entry point"""
        parser = self._create_parser()
        args = parser.parse_args()
        
        # Handle no arguments - show interactive menu
        if len(sys.argv) == 1:
            self._interactive_mode()
            return
        
        # Execute based on command
        try:
            if args.command == 'organize':
                self._handle_organize(args)
            elif args.command == 'config':
                self._handle_config(args)
            elif args.command == 'profiles':
                self._handle_profiles(args)
            elif args.command == 'logs':
                self._handle_logs(args)
            elif args.command == 'stats':
                self._handle_stats(args)
            elif args.command == 'undo':
                self._handle_undo(args)
            elif args.command == 'watch':
                self._handle_watch(args)
            elif args.command == 'clean':
                self._handle_clean(args)
            
        except KeyboardInterrupt:
            CLI.print_warning("Operation cancelled")
            sys.exit(1)
        except Exception as e:
            CLI.print_error(f"Error: {e}")
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser"""
        parser = argparse.ArgumentParser(
            description="File Organizer v2.0 - Professional file organization utility",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s                                    # Interactive mode
  %(prog)s organize --preview                 # Preview organization
  %(prog)s organize --path ~/Downloads        # Organize Downloads folder
  %(prog)s organize --profile photographer    # Use photographer profile
  %(prog)s config --create developer          # Create developer profile
  %(prog)s profiles --list                    # List available profiles
  %(prog)s logs --recent 5                    # Show 5 recent sessions
  %(prog)s stats --days 30                    # Show 30-day statistics
  %(prog)s undo                              # Undo last operation
  %(prog)s watch ~/Downloads                 # Watch folder for changes
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Organize command
        organize_parser = subparsers.add_parser('organize', help='Organize files')
        organize_parser.add_argument('--path', type=str, help='Target directory to organize')
        organize_parser.add_argument('--profile', type=str, help='Configuration profile to use')
        organize_parser.add_argument('--preview', action='store_true', help='Preview mode (no changes)')
        organize_parser.add_argument('--duplicates', action='store_true', help='Detect and handle duplicates')
        organize_parser.add_argument('--undo-info', action='store_true', help='Create undo information')
        organize_parser.add_argument('--threads', type=int, default=4, help='Number of threads to use')
        organize_parser.add_argument('--batch', action='store_true', help='Batch mode (no prompts)')
        
        # Config command
        config_parser = subparsers.add_parser('config', help='Manage configuration')
        config_group = config_parser.add_mutually_exclusive_group(required=True)
        config_group.add_argument('--interactive', action='store_true', help='Interactive configuration')
        config_group.add_argument('--create', type=str, help='Create profile (default/photographer/developer/student/business)')
        config_group.add_argument('--edit', type=str, help='Edit existing profile')
        config_group.add_argument('--validate', type=str, help='Validate profile')
        config_group.add_argument('--export', nargs=2, metavar=('PROFILE', 'FILE'), help='Export profile to file')
        config_group.add_argument('--import', type=str, help='Import profile from file')
        
        # Profiles command
        profiles_parser = subparsers.add_parser('profiles', help='Manage profiles')
        profiles_group = profiles_parser.add_mutually_exclusive_group(required=True)
        profiles_group.add_argument('--list', action='store_true', help='List all profiles')
        profiles_group.add_argument('--show', type=str, help='Show profile details')
        profiles_group.add_argument('--set', type=str, help='Set active profile')
        profiles_group.add_argument('--delete', type=str, help='Delete profile')
        profiles_group.add_argument('--copy', nargs=2, metavar=('FROM', 'TO'), help='Copy profile')
        
        # Logs command
        logs_parser = subparsers.add_parser('logs', help='View logs and history')
        logs_group = logs_parser.add_mutually_exclusive_group(required=True)
        logs_group.add_argument('--recent', type=int, default=5, help='Show recent sessions')
        logs_group.add_argument('--session', type=str, help='Show specific session')
        logs_group.add_argument('--errors', action='store_true', help='Show errors only')
        logs_group.add_argument('--search', type=str, help='Search logs')
        logs_group.add_argument('--export', nargs=2, metavar=('SESSION', 'FILE'), help='Export session to CSV')
        logs_group.add_argument('--cleanup', type=int, help='Clean up logs older than N days')
        
        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show statistics')
        stats_parser.add_argument('--days', type=int, default=30, help='Days to include in statistics')
        stats_parser.add_argument('--detailed', action='store_true', help='Show detailed statistics')
        
        # Undo command
        undo_parser = subparsers.add_parser('undo', help='Undo operations')
        undo_parser.add_argument('--file', type=str, default='undo_info.json', help='Undo file path')
        
        # Watch command
        watch_parser = subparsers.add_parser('watch', help='Watch directory for changes')
        watch_parser.add_argument('path', help='Directory to watch')
        watch_parser.add_argument('--profile', type=str, help='Profile to use for organization')
        watch_parser.add_argument('--interval', type=int, default=5, help='Check interval in seconds')
        
        # Clean command
        clean_parser = subparsers.add_parser('clean', help='Clean up application data')
        clean_group = clean_parser.add_mutually_exclusive_group(required=True)
        clean_group.add_argument('--logs', type=int, help='Clean logs older than N days')
        clean_group.add_argument('--all', action='store_true', help='Clean all temporary data')
        clean_group.add_argument('--cache', action='store_true', help='Clean cache files')
        
        return parser
    
    def _handle_organize(self, args):
        """Handle organize command"""
        CLI.print_logo()
        
        # Set up organizer
        if args.threads:
            self.organizer.max_threads = args.threads
        
        # Determine target directory
        target_dir = args.path
        if not target_dir:
            if args.profile:
                self.config_manager.set_active_profile(args.profile)
            profile = self.config_manager.get_active_profile()
            if profile:
                target_dir = profile.target_directory
            else:
                CLI.print_error("No target directory specified and no active profile")
                return
        
        # Validate directory
        if not Path(target_dir).exists():
            CLI.print_error(f"Directory does not exist: {target_dir}")
            return
        
        # Confirm in batch mode
        if not args.batch and not args.preview:
            if not CLI.confirm(f"Organize files in {target_dir}?", default=True):
                CLI.print_info("Operation cancelled")
                return
        
        # Run organization
        stats = self.organizer.organize_directory(
            target_directory=target_dir,
            profile_name=args.profile,
            dry_run=args.preview,
            enable_duplicates=args.duplicates,
            enable_undo=args.undo_info
        )
        
        # Show final stats
        if not args.preview:
            CLI.print_success(f"Organization complete! Processed {stats.total_files} files")
    
    def _handle_config(self, args):
        """Handle config command"""
        if args.interactive:
            self._config_interactive()
        elif args.create:
            self._config_create(args.create)
        elif args.edit:
            self._config_edit(args.edit)
        elif args.validate:
            self._config_validate(args.validate)
        elif args.export:
            self._config_export(args.export[0], args.export[1])
        elif getattr(args, 'import', None):
            self._config_import(getattr(args, 'import'))
    
    def _handle_profiles(self, args):
        """Handle profiles command"""
        if args.list:
            self._profiles_list()
        elif args.show:
            self._profiles_show(args.show)
        elif args.set:
            self._profiles_set(args.set)
        elif args.delete:
            self._profiles_delete(args.delete)
        elif args.copy:
            self._profiles_copy(args.copy[0], args.copy[1])
    
    def _handle_logs(self, args):
        """Handle logs command"""
        if args.recent:
            self._logs_recent(args.recent)
        elif args.session:
            self._logs_session(args.session)
        elif args.errors:
            self._logs_errors()
        elif args.search:
            self._logs_search(args.search)
        elif args.export:
            self._logs_export(args.export[0], args.export[1])
        elif args.cleanup:
            self._logs_cleanup(args.cleanup)
    
    def _handle_stats(self, args):
        """Handle stats command"""
        stats = self.logger.get_statistics(args.days)
        
        CLI.print_header(f"📊 STATISTICS - Last {args.days} Days")
        
        if not stats:
            CLI.print_info("No statistics available")
            return
        
        # Basic stats
        CLI.print_section("📋 Summary")
        CLI.print_info(f"Total Operations: {stats.get('total_operations', 0)}")
        CLI.print_info(f"Files Moved: {stats.get('files_moved', 0)}")
        CLI.print_info(f"Files Copied: {stats.get('files_copied', 0)}")
        CLI.print_info(f"Errors: {stats.get('errors', 0)}")
        
        # File categories
        categories = stats.get('categories', {})
        if categories:
            CLI.print_section("📁 File Categories")
            CLI.print_statistics(categories)
        
        # Session stats
        CLI.print_section("🕒 Session Statistics")
        CLI.print_info(f"Total Sessions: {stats.get('total_sessions', 0)}")
        CLI.print_info(f"Average Duration: {stats.get('avg_session_duration', 0):.1f} seconds")
        CLI.print_info(f"Average Files per Session: {stats.get('avg_files_per_session', 0):.1f}")
        
        if args.detailed:
            # Additional detailed stats would go here
            CLI.print_section("🔍 Detailed Statistics")
            CLI.print_info("Detailed statistics feature coming soon...")
    
    def _handle_undo(self, args):
        """Handle undo command"""
        CLI.print_header("↩️ UNDO OPERATION")
        
        if not Path(args.file).exists():
            CLI.print_error("No undo information found")
            return
        
        if CLI.confirm("Undo the last organization operation?", default=False):
            success = self.organizer.undo_last_operation(args.file)
            if success:
                CLI.print_success("Undo operation completed successfully")
            else:
                CLI.print_error("Undo operation failed")
    
    def _handle_watch(self, args):
        """Handle watch command"""
        CLI.print_header("👀 WATCH MODE")
        CLI.print_info(f"Watching directory: {args.path}")
        CLI.print_info("Press Ctrl+C to stop watching")
        
        try:
            import time
            watch_path = Path(args.path)
            
            if not watch_path.exists():
                CLI.print_error(f"Directory does not exist: {args.path}")
                return
            
            # Simple file watching implementation
            last_check = {}
            
            while not self.interrupted:
                try:
                    current_files = {}
                    for file_path in watch_path.rglob('*'):
                        if file_path.is_file():
                            stat_info = file_path.stat()
                            current_files[str(file_path)] = stat_info.st_mtime
                    
                    # Check for new or modified files
                    new_files = []
                    for file_path, mtime in current_files.items():
                        if file_path not in last_check or last_check[file_path] != mtime:
                            new_files.append(file_path)
                    
                    if new_files:
                        CLI.print_info(f"Detected {len(new_files)} new/modified files")
                        
                        if CLI.confirm("Organize new files?", default=True):
                            stats = self.organizer.organize_directory(
                                target_directory=args.path,
                                profile_name=args.profile,
                                dry_run=False
                            )
                            CLI.print_success(f"Organized {stats.files_moved} files")
                    
                    last_check = current_files
                    time.sleep(args.interval)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    CLI.print_error(f"Watch error: {e}")
                    time.sleep(args.interval)
        
        except ImportError:
            CLI.print_error("Watch feature requires additional dependencies")
            CLI.print_info("Consider installing 'watchdog' for better file monitoring")
    
    def _handle_clean(self, args):
        """Handle clean command"""
        CLI.print_header("🧹 CLEANUP")
        
        if args.logs:
            self.logger.cleanup_old_logs(args.logs)
            CLI.print_success(f"Cleaned up logs older than {args.logs} days")
        elif args.all:
            # Clean all temporary data
            self.logger.cleanup_old_logs(30)  # Keep 30 days
            # Clean undo files
            for undo_file in Path('.').glob('undo_info*.json'):
                undo_file.unlink()
                CLI.print_info(f"Removed {undo_file}")
            CLI.print_success("Cleanup complete")
        elif args.cache:
            # Clean cache files (if any)
            CLI.print_info("No cache files to clean")
    
    def _interactive_mode(self):
        """Interactive mode with menu system"""
        CLI.print_logo()
        
        while True:
            CLI.print_section("🚀 MAIN MENU")
            
            options = [
                "🗂️  Organize Files",
                "⚙️  Configuration Management", 
                "👤 Profile Management",
                "📊 View Logs & Statistics",
                "↩️  Undo Operations",
                "👀 Watch Directory",
                "🧹 Cleanup",
                "❓ Help",
                "🚪 Exit"
            ]
            
            choice = CLI.select_option("Select an option:", options)
            
            if choice == 0:  # Organize Files
                self._interactive_organize()
            elif choice == 1:  # Configuration
                self._interactive_config()
            elif choice == 2:  # Profiles
                self._interactive_profiles()
            elif choice == 3:  # Logs & Stats
                self._interactive_logs()
            elif choice == 4:  # Undo
                self._interactive_undo()
            elif choice == 5:  # Watch
                self._interactive_watch()
            elif choice == 6:  # Cleanup
                self._interactive_cleanup()
            elif choice == 7:  # Help
                self._show_help()
            elif choice == 8:  # Exit
                CLI.print_info("Goodbye! 👋")
                break
    
    def _interactive_organize(self):
        """Interactive file organization"""
        CLI.clear_screen()
        CLI.print_header("🗂️ FILE ORGANIZATION")
        
        # Get target directory
        current_profile = self.config_manager.get_active_profile()
        default_path = current_profile.target_directory if current_profile else str(Path.home() / "Downloads")
        
        target_dir = input(f"Target directory [{default_path}]: ").strip()
        if not target_dir:
            target_dir = default_path
        
        if not Path(target_dir).exists():
            CLI.print_error(f"Directory does not exist: {target_dir}")
            input("Press Enter to continue...")
            return
        
        # Select profile
        profiles = self.config_manager.get_profile_list()
        if profiles:
            CLI.print_info("\nAvailable profiles:")
            profile_choice = CLI.select_option("Select profile:", profiles)
            selected_profile = profiles[profile_choice]
        else:
            CLI.print_warning("No profiles available. Creating default profile...")
            self.config_manager.create_default_profile()
            selected_profile = "default"
        
        # Options
        preview_mode = CLI.confirm("Preview mode (no changes)?", default=True)
        detect_duplicates = CLI.confirm("Detect duplicate files?", default=False)
        create_undo = CLI.confirm("Create undo information?", default=True)
        
        # Execute organization
        try:
            stats = self.organizer.organize_directory(
                target_directory=target_dir,
                profile_name=selected_profile,
                dry_run=preview_mode,
                enable_duplicates=detect_duplicates,
                enable_undo=create_undo
            )
            
            CLI.print_success("Organization completed!")
            
        except Exception as e:
            CLI.print_error(f"Organization failed: {e}")
        
        input("\nPress Enter to continue...")
    
    def _interactive_config(self):
        """Interactive configuration management"""
        CLI.clear_screen()
        CLI.print_header("⚙️ CONFIGURATION MANAGEMENT")
        
        options = [
            "View Current Configuration",
            "Create New Profile", 
            "Edit Existing Profile",
            "Import/Export Profiles",
            "Back to Main Menu"
        ]
        
        choice = CLI.select_option("Select configuration option:", options)
        
        if choice == 0:  # View current
            profile = self.config_manager.get_active_profile()
            if profile:
                self._display_profile_details(profile)
            else:
                CLI.print_info("No active profile")
        
        elif choice == 1:  # Create new
            self._config_create_interactive()
        
        elif choice == 2:  # Edit existing
            profiles = self.config_manager.get_profile_list()
            if profiles:
                profile_choice = CLI.select_option("Select profile to edit:", profiles)
                self._config_edit(profiles[profile_choice])
            else:
                CLI.print_info("No profiles available")
        
        elif choice == 3:  # Import/Export
            self._config_import_export_interactive()
        
        elif choice == 4:  # Back
            return
        
        input("\nPress Enter to continue...")
    
    def _show_help(self):
        """Show help information"""
        CLI.clear_screen()
        CLI.print_header("❓ HELP & DOCUMENTATION")
        
        help_text = f"""
{Colors.BRIGHT_CYAN}File Organizer v2.0 Help{Colors.RESET}

{Colors.BOLD}BASIC USAGE:{Colors.RESET}
• Run without arguments for interactive mode
• Use 'organize --preview' to see what would be organized
• Use 'organize --path /your/path' to organize specific directory

{Colors.BOLD}COMMON COMMANDS:{Colors.RESET}
• organize --preview                 Preview file organization
• organize --path ~/Downloads        Organize Downloads folder
• profiles --list                    List available profiles
• logs --recent 5                    Show recent organization sessions
• config --create photographer       Create photographer profile
• undo                              Undo last organization

{Colors.BOLD}PROFILES:{Colors.RESET}
Profiles define how files are organized. Built-in profiles include:
• default     - General purpose organization
• photographer - Optimized for photos and media
• developer   - Optimized for code and development files
• student     - Optimized for academic work
• business    - Optimized for business documents

{Colors.BOLD}ADVANCED FEATURES:{Colors.RESET}
• Duplicate detection and handling
• Undo functionality
• Multi-threaded processing
• Directory watching
• Comprehensive logging
• Statistical analysis

{Colors.BOLD}SAFETY:{Colors.RESET}
• Always use --preview first to see what will happen
• Enable undo information for important operations
• Check logs for any errors or issues

{Colors.BOLD}SUPPORT:{Colors.RESET}
• GitHub: https://github.com/furqanahmadrao/python-file-organize-utility
• Check logs for detailed operation information
"""
        
        print(help_text)
        input("\nPress Enter to continue...")
    
    # Profile management methods
    def _profiles_list(self):
        """List all available profiles"""
        CLI.print_header("👤 AVAILABLE PROFILES")
        
        profiles = self.config_manager.get_profile_list()
        if not profiles:
            CLI.print_info("No profiles available")
            return
            
        current_profile = self.config_manager.get_active_profile()
        current_name = current_profile.name if current_profile else None
        
        for profile_name in sorted(profiles):
            profile = self.config_manager.get_profile(profile_name)
            if profile:
                marker = " (active)" if profile_name == current_name else ""
                CLI.print_info(f"• {profile_name}{marker} - {profile.description}")
    
    def _profiles_show(self, profile_name: str):
        """Show details of a specific profile"""
        profile = self.config_manager.get_profile(profile_name)
        if not profile:
            CLI.print_error(f"Profile '{profile_name}' not found")
            return
        
        self._display_profile_details(profile)
    
    def _profiles_set(self, profile_name: str):
        """Set active profile"""
        if self.config_manager.set_active_profile(profile_name):
            CLI.print_success(f"Active profile set to: {profile_name}")
        else:
            CLI.print_error(f"Profile '{profile_name}' not found")
    
    def _profiles_delete(self, profile_name: str):
        """Delete a profile"""
        if profile_name == "default":
            CLI.print_error("Cannot delete default profile")
            return
            
        if CLI.confirm(f"Delete profile '{profile_name}'?", default=False):
            # Note: Would need delete_profile method in ConfigManager
            CLI.print_warning(f"Profile deletion not implemented yet")
    
    def _profiles_copy(self, source: str, dest: str):
        """Copy a profile"""
        source_profile = self.config_manager.get_profile(source)
        if not source_profile:
            CLI.print_error(f"Source profile '{source}' not found")
            return
            
        # Create a copy with new name
        import copy
        new_profile = copy.deepcopy(source_profile)
        new_profile.name = dest
        new_profile.description = f"Copy of {source}"
        
        if self.config_manager.save_profile(new_profile):
            CLI.print_success(f"Profile copied: {source} → {dest}")
        else:
            CLI.print_error("Failed to copy profile")

    # Configuration management methods
    def _config_create(self, profile_type: str):
        """Create a new profile"""
        CLI.print_header(f"⚙️ CREATING {profile_type.upper()} PROFILE")
        
        profile = self.config_manager.create_profile_for_use_case(profile_type)
        if profile:
            CLI.print_success(f"Created {profile_type} profile: {profile.name}")
        else:
            CLI.print_error(f"Failed to create {profile_type} profile")
    
    def _config_edit(self, profile_name: str):
        """Edit an existing profile"""
        CLI.print_info(f"Interactive profile editing not implemented yet")
        CLI.print_info(f"Use export/import workflow to edit profile '{profile_name}'")
    
    def _config_validate(self, profile_name: str):
        """Validate a profile"""
        profile = self.config_manager.get_profile(profile_name)
        if not profile:
            CLI.print_error(f"Profile '{profile_name}' not found")
            return
            
        is_valid, errors = self.config_manager.validate_profile(profile)
        if is_valid:
            CLI.print_success(f"Profile '{profile_name}' is valid")
        else:
            CLI.print_error(f"Profile '{profile_name}' has issues:")
            for error in errors:
                CLI.print_error(f"  • {error}")
    
    def _config_export(self, profile_name: str, export_path: str):
        """Export a profile"""
        if self.config_manager.export_profile(profile_name, export_path):
            CLI.print_success(f"Profile '{profile_name}' exported to: {export_path}")
        else:
            CLI.print_error("Export failed")
    
    def _config_import(self, import_path: str):
        """Import a profile"""
        if self.config_manager.import_profile(import_path):
            CLI.print_success(f"Profile imported from: {import_path}")
        else:
            CLI.print_error("Import failed")

    # Logs management methods
    def _logs_recent(self, count: int):
        """Show recent sessions"""
        CLI.print_header(f"📊 RECENT SESSIONS ({count})")
        CLI.print_info("Recent logs feature not fully implemented yet")
        
    def _logs_session(self, session_id: str):
        """Show specific session"""
        CLI.print_header(f"📊 SESSION: {session_id}")
        CLI.print_info("Session details feature not fully implemented yet")
        
    def _logs_errors(self):
        """Show error logs only"""
        CLI.print_header("❌ ERROR LOGS")
        CLI.print_info("Error logs feature not fully implemented yet")
        
    def _logs_search(self, search_term: str):
        """Search logs"""
        CLI.print_header(f"🔍 SEARCH LOGS: {search_term}")
        CLI.print_info("Log search feature not fully implemented yet")
        
    def _logs_export(self, session_id: str, export_path: str):
        """Export session to CSV"""
        CLI.print_info(f"Exporting session {session_id} to {export_path}")
        CLI.print_info("Log export feature not fully implemented yet")
        
    def _logs_cleanup(self, days: int):
        """Clean up old logs"""
        CLI.print_info(f"Cleaning up logs older than {days} days")
        self.logger.cleanup_old_logs(days)
        CLI.print_success("Log cleanup completed")

    # Additional helper methods for interactive modes...
    def _config_create_interactive(self):
        """Interactive profile creation"""
        CLI.print_section("Creating New Profile")
        
        profile_types = ["default", "photographer", "developer", "student", "business", "custom"]
        choice = CLI.select_option("Select profile type:", profile_types)
        
        profile_type = profile_types[choice]
        
        if profile_type == "custom":
            CLI.print_info("Custom profile creation requires manual configuration")
            CLI.print_info("Use 'config --create default' and then edit the created profile")
        else:
            profile = self.config_manager.create_profile_for_use_case(profile_type)
            if profile:
                CLI.print_success(f"Created profile: {profile.name}")
                self._display_profile_details(profile)
    
    def _display_profile_details(self, profile):
        """Display profile details"""
        CLI.print_section(f"Profile: {profile.name}")
        CLI.print_info(f"Description: {profile.description}")
        CLI.print_info(f"Target Directory: {profile.target_directory}")
        CLI.print_info(f"Organization Method: {profile.organize_by.value}")
        CLI.print_info(f"Rules: {len(profile.rules)} categories")
        
        for rule in profile.rules[:5]:  # Show first 5 rules
            ext_display = ", ".join(rule.extensions[:3])
            if len(rule.extensions) > 3:
                ext_display += f" ... (+{len(rule.extensions)-3} more)"
            CLI.print_info(f"  • {rule.name}: {ext_display}")
        
        if len(profile.rules) > 5:
            CLI.print_info(f"  ... and {len(profile.rules)-5} more rules")


def main():
    """Main entry point"""
    try:
        app = EnhancedCLI()
        app.run()
    except KeyboardInterrupt:
        CLI.print_warning("\nOperation cancelled")
        sys.exit(1)
    except Exception as e:
        CLI.print_error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()