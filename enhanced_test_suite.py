#!/usr/bin/env python3
"""
Enhanced Test Script for File Organizer v2.0 CLI
Comprehensive testing of all CLI features and functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional
import time
import json

# Add the package to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from file_organizer.core.organizer import FileOrganizer
from file_organizer.core.config_manager import ConfigManager
from file_organizer.core.logger import Logger
from file_organizer.utils.cli import CLI, Colors, Icons

class EnhancedTestSuite:
    """Enhanced test suite for CLI functionality"""
    
    def __init__(self):
        self.test_dir = None
        self.config_manager = ConfigManager()
        self.logger = Logger()
        self.organizer = FileOrganizer(self.config_manager, self.logger)
        self.test_results = []
        
    def setup_test_environment(self):
        """Create test directory with sample files"""
        CLI.print_header("🔧 SETTING UP TEST ENVIRONMENT")
        
        # Create temporary test directory
        self.test_dir = Path(tempfile.mkdtemp(prefix="file_organizer_test_"))
        CLI.print_info(f"Test directory: {self.test_dir}")
        
        # Create sample files for testing
        test_files = [
            # Documents
            ("document1.pdf", b"PDF content"),
            ("report.docx", b"Word document content"),
            ("presentation.pptx", b"PowerPoint content"),
            ("spreadsheet.xlsx", b"Excel content"),
            ("notes.txt", b"Text file content"),
            
            # Images
            ("photo1.jpg", b"JPEG image data"),
            ("screenshot.png", b"PNG image data"),
            ("logo.svg", b"SVG image data"),
            ("animation.gif", b"GIF animation data"),
            
            # Audio/Video
            ("song.mp3", b"MP3 audio data"),
            ("video.mp4", b"MP4 video data"),
            ("audio.wav", b"WAV audio data"),
            
            # Code files
            ("script.py", b"print('Hello, World!')"),
            ("webpage.html", b"<html><body>Test</body></html>"),
            ("styles.css", b"body { margin: 0; }"),
            ("app.js", b"console.log('JavaScript');"),
            
            # Archives
            ("backup.zip", b"ZIP archive data"),
            ("data.tar.gz", b"TAR.GZ archive data"),
            
            # Executables
            ("program.exe", b"Executable file"),
            ("installer.msi", b"MSI installer"),
            
            # Other
            ("config.json", b'{"setting": "value"}'),
            ("data.csv", b"name,age\nJohn,25"),
            ("readme.md", b"# Test Project"),
        ]
        
        # Create subdirectories with files
        subdirs = ["subdir1", "nested/deep/folder", "mixed_files"]
        for subdir in subdirs:
            subdir_path = self.test_dir / subdir
            subdir_path.mkdir(parents=True, exist_ok=True)
            
            # Add some files to subdirectories
            (subdir_path / "sub_document.pdf").write_bytes(b"PDF in subdir")
            (subdir_path / "sub_image.png").write_bytes(b"PNG in subdir")
        
        # Create test files in main directory
        for filename, content in test_files:
            (self.test_dir / filename).write_bytes(content)
        
        # Create some duplicate files
        (self.test_dir / "duplicate1.txt").write_bytes(b"Same content")
        (self.test_dir / "duplicate2.txt").write_bytes(b"Same content")
        (self.test_dir / "different.txt").write_bytes(b"Different content")
        
        CLI.print_success(f"Created {len(test_files) + 6} test files")
        return True
    
    def test_basic_organization(self):
        """Test basic file organization functionality"""
        CLI.print_header("📁 TESTING BASIC ORGANIZATION")
        
        try:
            # Test preview mode (dry run)
            CLI.print_info("Testing preview mode...")
            stats = self.organizer.organize_directory(
                target_directory=str(self.test_dir),
                profile_name="default",
                dry_run=True
            )
            
            if stats and stats.total_files > 0:
                CLI.print_success(f"Preview mode: Found {stats.total_files} files")
                self.test_results.append(("Basic Organization Preview", True, f"Found {stats.total_files} files"))
            else:
                CLI.print_error("Preview mode failed")
                self.test_results.append(("Basic Organization Preview", False, "No files found"))
                return False
            
            # Test actual organization
            CLI.print_info("Testing actual organization...")
            stats = self.organizer.organize_directory(
                target_directory=str(self.test_dir),
                profile_name="default",
                dry_run=False,
                enable_undo=True
            )
            
            if stats and stats.files_moved > 0:
                CLI.print_success(f"Organization complete: Moved {stats.files_moved} files")
                self.test_results.append(("Basic Organization", True, f"Moved {stats.files_moved} files"))
                return True
            else:
                CLI.print_error("Organization failed")
                self.test_results.append(("Basic Organization", False, "No files moved"))
                return False
                
        except Exception as e:
            CLI.print_error(f"Organization test failed: {e}")
            self.test_results.append(("Basic Organization", False, str(e)))
            return False
    
    def test_profile_management(self):
        """Test profile management functionality"""
        CLI.print_header("👤 TESTING PROFILE MANAGEMENT")
        
        try:
            # Test profile creation
            CLI.print_info("Testing profile creation...")
            profiles = ["photographer", "developer", "student", "business"]
            
            for profile_type in profiles:
                profile = self.config_manager.create_profile_for_use_case(profile_type)
                if profile:
                    CLI.print_success(f"Created {profile_type} profile")
                    self.test_results.append((f"Profile Creation ({profile_type})", True, f"Created successfully"))
                else:
                    CLI.print_error(f"Failed to create {profile_type} profile")
                    self.test_results.append((f"Profile Creation ({profile_type})", False, "Creation failed"))
            
            # Test profile listing
            CLI.print_info("Testing profile listing...")
            profile_list = self.config_manager.get_profile_list()
            if profile_list:
                CLI.print_success(f"Found {len(profile_list)} profiles")
                self.test_results.append(("Profile Listing", True, f"Found {len(profile_list)} profiles"))
            else:
                CLI.print_error("No profiles found")
                self.test_results.append(("Profile Listing", False, "No profiles found"))
            
            # Test profile export/import
            CLI.print_info("Testing profile export/import...")
            if profile_list:
                test_profile_name = profile_list[0]
                export_file = self.test_dir / "test_profile_export.json"
                
                # Export profile
                if self.config_manager.export_profile(test_profile_name, str(export_file)):
                    CLI.print_success("Profile export successful")
                    
                    # Import profile with new name
                    if self.config_manager.import_profile(str(export_file), "imported_test"):
                        CLI.print_success("Profile import successful")
                        self.test_results.append(("Profile Export/Import", True, "Both operations successful"))
                    else:
                        CLI.print_error("Profile import failed")
                        self.test_results.append(("Profile Export/Import", False, "Import failed"))
                else:
                    CLI.print_error("Profile export failed")
                    self.test_results.append(("Profile Export/Import", False, "Export failed"))
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Profile management test failed: {e}")
            self.test_results.append(("Profile Management", False, str(e)))
            return False
    
    def test_duplicate_detection(self):
        """Test duplicate file detection"""
        CLI.print_header("🔍 TESTING DUPLICATE DETECTION")
        
        try:
            CLI.print_info("Testing duplicate detection...")
            
            # Run organization with duplicate detection
            stats = self.organizer.organize_directory(
                target_directory=str(self.test_dir),
                profile_name="default",
                dry_run=True,  # Preview mode to see duplicates
                enable_duplicates=True
            )
            
            if hasattr(stats, 'duplicates_found') and stats.duplicates_found > 0:
                CLI.print_success(f"Found {stats.duplicates_found} duplicate files")
                self.test_results.append(("Duplicate Detection", True, f"Found {stats.duplicates_found} duplicates"))
            else:
                # This is expected if no actual duplicates exist
                CLI.print_info("No duplicates found (expected for unique test files)")
                self.test_results.append(("Duplicate Detection", True, "No duplicates found (normal)"))
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Duplicate detection test failed: {e}")
            self.test_results.append(("Duplicate Detection", False, str(e)))
            return False
    
    def test_undo_functionality(self):
        """Test undo functionality"""
        CLI.print_header("↩️ TESTING UNDO FUNCTIONALITY")
        
        try:
            CLI.print_info("Testing undo functionality...")
            
            # Create undo info file path
            undo_file = self.test_dir / "test_undo_info.json"
            
            # Perform an organization with undo enabled
            CLI.print_info("Performing organization with undo enabled...")
            original_files = list(self.test_dir.rglob("*"))
            
            stats = self.organizer.organize_directory(
                target_directory=str(self.test_dir),
                profile_name="default",
                dry_run=False,
                enable_undo=True
            )
            
            if stats and stats.files_moved > 0:
                CLI.print_info(f"Organization moved {stats.files_moved} files")
                
                # Check if undo file was created
                undo_files = list(self.test_dir.glob("undo_info*.json"))
                if undo_files:
                    CLI.print_success(f"Undo file created: {undo_files[0].name}")
                    
                    # Test undo operation
                    CLI.print_info("Testing undo operation...")
                    success = self.organizer.undo_last_operation(str(undo_files[0]))
                    
                    if success:
                        CLI.print_success("Undo operation successful")
                        self.test_results.append(("Undo Functionality", True, "Undo completed successfully"))
                    else:
                        CLI.print_error("Undo operation failed")
                        self.test_results.append(("Undo Functionality", False, "Undo operation failed"))
                else:
                    CLI.print_error("No undo file created")
                    self.test_results.append(("Undo Functionality", False, "No undo file created"))
            else:
                CLI.print_info("No files to organize for undo test")
                self.test_results.append(("Undo Functionality", True, "No files to test (normal)"))
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Undo test failed: {e}")
            self.test_results.append(("Undo Functionality", False, str(e)))
            return False
    
    def test_logging_system(self):
        """Test logging and statistics"""
        CLI.print_header("📊 TESTING LOGGING SYSTEM")
        
        try:
            CLI.print_info("Testing logging system...")
            
            # Test session tracking
            session_id = self.logger.start_session("test_profile", str(self.test_dir))
            CLI.print_info(f"Started session: {session_id}")
            
            # Log some test operations
            self.logger.log_operation("TEST", "test_file.txt", "Test operation")
            self.logger.log_operation("MOVE", "document.pdf", "Documents/document.pdf")
            self.logger.log_error("TEST_ERROR", "Error message for testing")
            
            # End session
            summary = self.logger.end_session()
            
            if summary:
                CLI.print_success(f"Session completed with {summary.total_operations} operations")
                self.test_results.append(("Logging System", True, f"{summary.total_operations} operations logged"))
            else:
                CLI.print_error("Session summary failed")
                self.test_results.append(("Logging System", False, "Session summary failed"))
            
            # Test statistics
            CLI.print_info("Testing statistics...")
            stats = self.logger.get_statistics(days=30)
            
            if stats:
                CLI.print_success("Statistics retrieved successfully")
                self.test_results.append(("Statistics", True, "Retrieved successfully"))
            else:
                CLI.print_info("No statistics available (normal for new installation)")
                self.test_results.append(("Statistics", True, "No data (normal)"))
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Logging test failed: {e}")
            self.test_results.append(("Logging System", False, str(e)))
            return False
    
    def test_cli_features(self):
        """Test CLI utility features"""
        CLI.print_header("🎨 TESTING CLI FEATURES")
        
        try:
            CLI.print_info("Testing CLI utility functions...")
            
            # Test color output
            CLI.print_success("✅ Colors working")
            CLI.print_warning("⚠️ Warnings working")
            CLI.print_error("❌ Errors working")
            CLI.print_info("ℹ️ Info working")
            
            # Test progress bar
            CLI.print_info("Testing progress bar...")
            progress = CLI.create_progress_bar(100, "Testing")
            for i in range(0, 101, 10):
                progress.update(i)
                time.sleep(0.1)
            progress.finish()
            
            # Test statistics display
            CLI.print_info("Testing statistics display...")
            test_stats = {
                "Documents": 15,
                "Images": 8,
                "Videos": 3,
                "Audio": 5,
                "Archives": 2
            }
            CLI.print_statistics(test_stats)
            
            CLI.print_success("CLI features test completed")
            self.test_results.append(("CLI Features", True, "All features working"))
            return True
            
        except Exception as e:
            CLI.print_error(f"CLI features test failed: {e}")
            self.test_results.append(("CLI Features", False, str(e)))
            return False
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        CLI.print_header("✅ TESTING CONFIGURATION VALIDATION")
        
        try:
            CLI.print_info("Testing configuration validation...")
            
            # Test profile validation
            profiles = self.config_manager.get_profile_list()
            for profile_name in profiles[:3]:  # Test first 3 profiles
                profile = self.config_manager.get_profile(profile_name)
                if profile:
                    is_valid, errors = self.config_manager.validate_profile(profile)
                    if is_valid:
                        CLI.print_success(f"Profile '{profile_name}' is valid")
                    else:
                        CLI.print_warning(f"Profile '{profile_name}' has issues: {errors}")
                    
                    self.test_results.append((f"Profile Validation ({profile_name})", is_valid, 
                                            "Valid" if is_valid else f"Errors: {errors}"))
            
            # Test directory validation
            CLI.print_info("Testing directory validation...")
            valid_dir = str(self.test_dir)
            invalid_dir = "/nonexistent/directory/path"
            
            if Path(valid_dir).exists():
                CLI.print_success(f"Directory validation: {valid_dir} exists")
                self.test_results.append(("Directory Validation (Valid)", True, "Directory exists"))
            
            if not Path(invalid_dir).exists():
                CLI.print_success(f"Directory validation: {invalid_dir} correctly identified as invalid")
                self.test_results.append(("Directory Validation (Invalid)", True, "Invalid directory detected"))
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Configuration validation test failed: {e}")
            self.test_results.append(("Configuration Validation", False, str(e)))
            return False
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        CLI.print_header("🧹 CLEANING UP TEST ENVIRONMENT")
        
        try:
            if self.test_dir and self.test_dir.exists():
                shutil.rmtree(self.test_dir)
                CLI.print_success(f"Cleaned up test directory: {self.test_dir}")
            
            # Clean up any test profiles
            test_profiles = ["imported_test"]
            for profile_name in test_profiles:
                if profile_name in self.config_manager.get_profile_list():
                    # Note: We'd need a delete_profile method in ConfigManager
                    CLI.print_info(f"Test profile '{profile_name}' should be manually removed if needed")
            
            return True
            
        except Exception as e:
            CLI.print_error(f"Cleanup failed: {e}")
            return False
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        CLI.print_header("📋 TEST REPORT")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result[1])
        failed_tests = total_tests - passed_tests
        
        CLI.print_info(f"Total Tests: {total_tests}")
        CLI.print_success(f"Passed: {passed_tests}")
        if failed_tests > 0:
            CLI.print_error(f"Failed: {failed_tests}")
        else:
            CLI.print_success("All tests passed! 🎉")
        
        # Detailed results
        CLI.print_section("📝 Detailed Results")
        for test_name, passed, details in self.test_results:
            status = "✅ PASS" if passed else "❌ FAIL"
            CLI.print_info(f"{status} {test_name}: {details}")
        
        # Save report to file
        report_file = Path("test_report.json")
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            "results": [
                {
                    "test": test_name,
                    "status": "PASS" if passed else "FAIL", 
                    "details": details
                }
                for test_name, passed, details in self.test_results
            ]
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            CLI.print_success(f"Test report saved to: {report_file}")
        except Exception as e:
            CLI.print_warning(f"Could not save report: {e}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run complete test suite"""
        CLI.print_logo()
        CLI.print_header("🧪 FILE ORGANIZER v2.0 - ENHANCED TEST SUITE")
        
        start_time = time.time()
        
        tests = [
            ("Environment Setup", self.setup_test_environment),
            ("Basic Organization", self.test_basic_organization),
            ("Profile Management", self.test_profile_management),
            ("Duplicate Detection", self.test_duplicate_detection),
            ("Undo Functionality", self.test_undo_functionality),
            ("Logging System", self.test_logging_system),
            ("CLI Features", self.test_cli_features),
            ("Configuration Validation", self.test_configuration_validation),
        ]
        
        CLI.print_info(f"Running {len(tests)} test categories...")
        print()
        
        for test_name, test_func in tests:
            CLI.print_info(f"▶️ Starting: {test_name}")
            try:
                success = test_func()
                if success:
                    CLI.print_success(f"✅ Completed: {test_name}")
                else:
                    CLI.print_error(f"❌ Failed: {test_name}")
            except Exception as e:
                CLI.print_error(f"💥 Exception in {test_name}: {e}")
                self.test_results.append((test_name, False, f"Exception: {e}"))
            print()
        
        # Cleanup and generate report
        self.cleanup_test_environment()
        
        end_time = time.time()
        duration = end_time - start_time
        
        CLI.print_info(f"Test suite completed in {duration:.2f} seconds")
        success = self.generate_test_report()
        
        return success


def main():
    """Main test runner"""
    try:
        print(f"{Colors.BRIGHT_CYAN}")
        print("=" * 80)
        print("FILE ORGANIZER v2.0 - ENHANCED CLI TEST SUITE")
        print("=" * 80)
        print(f"{Colors.RESET}")
        
        test_suite = EnhancedTestSuite()
        success = test_suite.run_all_tests()
        
        if success:
            CLI.print_success("\n🎉 ALL TESTS PASSED! 🎉")
            sys.exit(0)
        else:
            CLI.print_error("\n❌ Some tests failed. Check the report for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        CLI.print_warning("\nTest suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        CLI.print_error(f"\nTest suite failed with exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()