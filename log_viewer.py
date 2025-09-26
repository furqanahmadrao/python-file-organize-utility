#!/usr/bin/env python3
"""
Log Viewer Tool for File Organizer v1.0
Display and analyze organization logs in a readable format
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Tuple
import argparse

class LogViewer:
    def __init__(self, log_file: str = "log.txt"):
        self.log_file = log_file
        self.sessions = []
        self.total_files_moved = 0
        self.total_errors = 0

    def load_log(self) -> bool:
        """Load and parse the log file"""
        if not os.path.exists(self.log_file):
            print(f"❌ Log file not found: {self.log_file}")
            return False
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"📄 Log file is empty: {self.log_file}")
                return False
            
            self.parse_sessions(content)
            return True
        
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
            return False

    def parse_sessions(self, content: str):
        """Parse log content into sessions"""
        # Split by session headers
        session_blocks = re.split(r'={60}', content)
        
        for block in session_blocks:
            if not block.strip():
                continue
            
            lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
            if not lines:
                continue
            
            # Look for session header
            session_header = None
            for line in lines:
                if "ORGANIZATION SESSION:" in line:
                    session_header = line.replace("ORGANIZATION SESSION:", "").strip()
                    break
            
            if not session_header:
                continue
            
            # Parse session data
            session = {
                'timestamp': session_header,
                'moves': [],
                'errors': [],
                'summary': {'moved': 0, 'errors': 0}
            }
            
            in_errors_section = False
            
            for line in lines[1:]:  # Skip the header line
                if line.startswith('ERRORS:'):
                    in_errors_section = True
                    continue
                elif line.startswith('SUMMARY:'):
                    # Parse summary
                    summary_match = re.search(r'(\d+) moved, (\d+) errors', line)
                    if summary_match:
                        session['summary']['moved'] = int(summary_match.group(1))
                        session['summary']['errors'] = int(summary_match.group(2))
                    continue
                
                # Parse log entries
                if ' | MOVED: ' in line:
                    session['moves'].append(line)
                elif ' | ERROR' in line or (in_errors_section and line):
                    session['errors'].append(line)
            
            self.sessions.append(session)
        
        # Calculate totals
        self.total_files_moved = sum(session['summary']['moved'] for session in self.sessions)
        self.total_errors = sum(session['summary']['errors'] for session in self.sessions)

    def display_summary(self):
        """Display overall summary of all sessions"""
        print("📊 LOG SUMMARY")
        print("=" * 30)
        print(f"📁 Total Sessions: {len(self.sessions)}")
        print(f"✅ Total Files Moved: {self.total_files_moved}")
        print(f"❌ Total Errors: {self.total_errors}")
        
        if self.sessions:
            latest_session = max(self.sessions, key=lambda x: x['timestamp'])
            print(f"🕒 Latest Session: {latest_session['timestamp']}")
        
        print()

    def display_recent_session(self, limit: int = 1):
        """Display the most recent session(s)"""
        if not self.sessions:
            print("📄 No sessions found in log file")
            return
        
        # Sort sessions by timestamp (most recent first)
        sorted_sessions = sorted(self.sessions, key=lambda x: x['timestamp'], reverse=True)
        sessions_to_show = sorted_sessions[:limit]
        
        for i, session in enumerate(sessions_to_show):
            print(f"🕒 SESSION {i+1}: {session['timestamp']}")
            print("-" * 50)
            
            if session['moves']:
                print("✅ FILES MOVED:")
                for move in session['moves']:
                    # Extract just the move part (after timestamp)
                    move_info = move.split(' | MOVED: ', 1)[-1]
                    print(f"   • {move_info}")
            
            if session['errors']:
                print("\n❌ ERRORS:")
                for error in session['errors']:
                    error_info = error.split(' | ', 1)[-1]
                    print(f"   • {error_info}")
            
            print(f"\n📊 Session Summary: {session['summary']['moved']} moved, {session['summary']['errors']} errors")
            
            if i < len(sessions_to_show) - 1:
                print("\n" + "="*50 + "\n")

    def display_all_sessions(self):
        """Display all sessions"""
        if not self.sessions:
            print("📄 No sessions found in log file")
            return
        
        # Sort sessions by timestamp (oldest first for full history)
        sorted_sessions = sorted(self.sessions, key=lambda x: x['timestamp'])
        
        for i, session in enumerate(sorted_sessions, 1):
            print(f"🕒 SESSION {i}: {session['timestamp']}")
            print("-" * 30)
            
            if session['moves']:
                print(f"✅ Files Moved ({len(session['moves'])}):")
                for move in session['moves']:
                    move_info = move.split(' | MOVED: ', 1)[-1]
                    print(f"   • {move_info}")
            else:
                print("✅ No files moved in this session")
            
            if session['errors']:
                print(f"\n❌ Errors ({len(session['errors'])}):")
                for error in session['errors']:
                    error_info = error.split(' | ', 1)[-1]
                    print(f"   • {error_info}")
            
            print(f"\n📊 Summary: {session['summary']['moved']} moved, {session['summary']['errors']} errors")
            
            if i < len(sorted_sessions):
                print("\n" + "="*50 + "\n")

    def display_errors_only(self):
        """Display only sessions with errors"""
        error_sessions = [s for s in self.sessions if s['errors']]
        
        if not error_sessions:
            print("✅ No errors found in log history!")
            return
        
        print(f"❌ SESSIONS WITH ERRORS ({len(error_sessions)} found)")
        print("=" * 40)
        
        for i, session in enumerate(error_sessions, 1):
            print(f"🕒 SESSION {i}: {session['timestamp']}")
            print("-" * 30)
            
            for error in session['errors']:
                error_info = error.split(' | ', 1)[-1]
                print(f"   • {error_info}")
            
            print(f"📊 Total errors in this session: {len(session['errors'])}")
            
            if i < len(error_sessions):
                print("\n" + "-"*30 + "\n")

    def display_statistics(self):
        """Display detailed statistics"""
        if not self.sessions:
            print("📄 No data available for statistics")
            return
        
        print("📈 DETAILED STATISTICS")
        print("=" * 40)
        
        # Category statistics
        category_stats = {}
        for session in self.sessions:
            for move in session['moves']:
                if ' → ' in move:
                    # Extract category from "filename → category/filename"
                    move_info = move.split(' | MOVED: ', 1)[-1]
                    if ' → ' in move_info:
                        category = move_info.split(' → ')[1].split('/')[0]
                        category_stats[category] = category_stats.get(category, 0) + 1
        
        if category_stats:
            print("📁 Files per Category:")
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {category}: {count} files")
        
        # Session statistics
        print(f"\n🕒 Session Statistics:")
        print(f"   Total Sessions: {len(self.sessions)}")
        print(f"   Average Files per Session: {self.total_files_moved / len(self.sessions):.1f}")
        
        if self.total_errors > 0:
            error_rate = (self.total_errors / (self.total_files_moved + self.total_errors)) * 100
            print(f"   Error Rate: {error_rate:.1f}%")
        else:
            print(f"   Error Rate: 0.0% ✅")
        
        # Date range
        if len(self.sessions) > 1:
            dates = [session['timestamp'] for session in self.sessions]
            print(f"\n📅 Activity Range:")
            print(f"   First Session: {min(dates)}")
            print(f"   Latest Session: {max(dates)}")

    def search_logs(self, search_term: str):
        """Search for specific files or patterns in logs"""
        print(f"🔍 SEARCHING FOR: '{search_term}'")
        print("=" * 40)
        
        found_results = []
        
        for session in self.sessions:
            session_results = []
            
            # Search in moves
            for move in session['moves']:
                if search_term.lower() in move.lower():
                    session_results.append(('MOVED', move))
            
            # Search in errors
            for error in session['errors']:
                if search_term.lower() in error.lower():
                    session_results.append(('ERROR', error))
            
            if session_results:
                found_results.append((session['timestamp'], session_results))
        
        if not found_results:
            print(f"❌ No results found for '{search_term}'")
            return
        
        print(f"✅ Found {sum(len(results) for _, results in found_results)} results in {len(found_results)} sessions:")
        print()
        
        for session_time, results in found_results:
            print(f"🕒 {session_time}")
            print("-" * 30)
            
            for result_type, result_text in results:
                if result_type == 'MOVED':
                    move_info = result_text.split(' | MOVED: ', 1)[-1]
                    print(f"   ✅ {move_info}")
                else:
                    error_info = result_text.split(' | ', 1)[-1]
                    print(f"   ❌ {error_info}")
            
            print()

    def clear_logs(self):
        """Clear the log file after confirmation"""
        if not os.path.exists(self.log_file):
            print(f"❌ Log file not found: {self.log_file}")
            return
        
        print("⚠️  WARNING: This will permanently delete all log history!")
        confirm = input("Are you sure you want to clear all logs? Type 'yes' to confirm: ")
        
        if confirm.lower() == 'yes':
            try:
                os.remove(self.log_file)
                print("✅ Log file cleared successfully")
                self.sessions = []
                self.total_files_moved = 0
                self.total_errors = 0
            except Exception as e:
                print(f"❌ Error clearing log file: {e}")
        else:
            print("❌ Log clearing cancelled")

    def interactive_menu(self):
        """Interactive menu for log viewing"""
        while True:
            print("\n" + "="*50)
            print("📋 FILE ORGANIZER - LOG VIEWER")
            print("="*50)
            
            print("1. 📊 Show summary")
            print("2. 🕒 Show recent session")
            print("3. 📜 Show all sessions")
            print("4. ❌ Show errors only")
            print("5. 📈 Show statistics")
            print("6. 🔍 Search logs")
            print("7. 🗑️  Clear logs")
            print("8. 🔄 Reload logs")
            print("9. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == "1":
                self.display_summary()
            elif choice == "2":
                try:
                    limit = int(input("How many recent sessions to show? (default: 1): ") or "1")
                    self.display_recent_session(limit)
                except ValueError:
                    self.display_recent_session()
            elif choice == "3":
                self.display_all_sessions()
            elif choice == "4":
                self.display_errors_only()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                search_term = input("Enter search term: ").strip()
                if search_term:
                    self.search_logs(search_term)
                else:
                    print("❌ Search term cannot be empty")
            elif choice == "7":
                self.clear_logs()
            elif choice == "8":
                if self.load_log():
                    print("✅ Logs reloaded successfully")
                else:
                    print("❌ Failed to reload logs")
            elif choice == "9":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-9.")
            
            if choice != "9":
                input("\nPress Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description='Log Viewer for File Organizer v1.0')
    parser.add_argument('--file', type=str, default='log.txt', help='Path to log file')
    parser.add_argument('--summary', action='store_true', help='Show summary and exit')
    parser.add_argument('--recent', type=int, help='Show N recent sessions and exit')
    parser.add_argument('--errors', action='store_true', help='Show errors only and exit')
    parser.add_argument('--search', type=str, help='Search for term and exit')
    parser.add_argument('--stats', action='store_true', help='Show statistics and exit')
    
    args = parser.parse_args()
    
    print("📋 FILE ORGANIZER v1.0 - LOG VIEWER")
    print("=" * 40)
    
    viewer = LogViewer(args.file)
    
    if not viewer.load_log():
        return
    
    # Handle command-line arguments for direct output
    if args.summary:
        viewer.display_summary()
    elif args.recent is not None:
        viewer.display_recent_session(args.recent)
    elif args.errors:
        viewer.display_errors_only()
    elif args.search:
        viewer.search_logs(args.search)
    elif args.stats:
        viewer.display_statistics()
    else:
        # No specific command, show interactive menu
        viewer.interactive_menu()

if __name__ == "__main__":
    main()